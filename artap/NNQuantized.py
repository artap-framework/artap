import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.sparse import csr_matrix
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler, TensorBoard, ModelCheckpoint
from tensorflow.keras.layers import InputSpec, Layer, Dense, Conv2D, BatchNormalization, MaxPooling2D, Activation
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import squared_hinge
from tensorflow.keras import backend as K
import tensorflow._api.v2.compat as tv

# tv.disable_v2_behavior()
tv.v1.disable_v2_behavior()
from tensorflow.keras.models import Sequential
from matplotlib import pyplot as plt
from tensorflow.keras import constraints
from tensorflow.keras import initializers
from artap.problem import Problem

'''
    paper: Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding.
    url : https://arxiv.org/abs/1510.00149
    The goal is to compress the neural network using weights quantization with no loss of accuracy.
'''


class LayerTrain(object):

    def __init__(self, in_depth, out_depth, N_clusters, name):
        self.clusters_masks = []
        self.name = name
        if 'conv' in name:
            self.w = tf.Variable(tf.random.normal([5, 5, in_depth, out_depth], stddev=0.1))

        elif 'fc' in name:
            self.w = tf.Variable(tf.random.normal([in_depth, out_depth], stddev=0.1))

        self.w_PH = tv.v1.placeholder(tf.float32, self.w.shape)
        self.assign_w = tv.v1.assign(self.w, self.w_PH)
        self.num_total_weights = np.prod(self.w.shape)

        # mask placeholder for pruning
        # ones - valid weights, zero - pruned weights
        self.pruning_mask_data = np.ones(self.w.shape, dtype=np.float32)
        self.N_clusters = N_clusters  # for quantization

    def forward(self, x):
        if 'conv' in self.name:
            return tf.nn.conv2d(x, self.w, strides=[1, 2, 2, 1], padding='SAME')

        elif 'fc' in self.name:
            return tf.matmul(x, self.w)

    def save_weights_histogram(self, sess, directory, iteration):
        w_data = sess.run(self.w).reshape(-1)
        valid_w_data = [x for x in w_data if x != 0.0]

        plt.grid(True)
        plt.hist(valid_w_data, 100, color='0.4')
        plt.gca().set_xlim([-0.4, 0.4])
        plt.savefig(directory + '/' + self.name + '-' + str(iteration), dpi=100)
        plt.gcf().clear()

    def save_weights(self, sess, directory):

        w_data = sess.run(self.w)
        np.save(directory + '/' + self.name + '-weights', w_data)
        np.save(directory + '/' + self.name + '-prune-mask', self.pruning_mask_data)

    # quantization
    def quantize_weights(self, sess):
        global distances
        w_data = sess.run(self.w)
        # theoretically pruning mask should be taken into consideration to compute max and min data only among valid
        # weights but in practice with normal ditribution init there is 100% chances that min and max vals will be
        # among valid weights
        max_val = np.max(w_data)
        min_val = np.min(w_data)

        # linearly initialize centroids between max and min
        self.centroids = np.linspace(min_val, max_val, self.N_clusters)
        w_data = np.expand_dims(w_data, 0)
        centroids_prev = np.copy(self.centroids)
        for i in range(20):
            if 'conv' in self.name:
                distances = np.abs(w_data - np.reshape(self.centroids, (-1, 1, 1, 1, 1)))
                distances = np.transpose(distances, (1, 2, 3, 4, 0))

            elif 'fc' in self.name:
                distances = np.abs(w_data - np.reshape(self.centroids, (-1, 1, 1)))
                distances = np.transpose(distances, (1, 2, 0))

            classes = np.argmin(distances, axis=-1)
            for i in range(self.N_clusters):
                cluster_mask = (classes == i).astype(np.float32) * self.pruning_mask_data
                self.clusters_masks.append(cluster_mask)

                num_weights_assigned = np.sum(cluster_mask)
                if num_weights_assigned != 0:
                    self.centroids[i] = np.sum(cluster_mask * w_data) / num_weights_assigned
                else:  # do not modify
                    pass
            if np.array_equal(centroids_prev, self.centroids):
                break

            centroids_prev = np.copy(self.centroids)

        self.quantize_weights_update(sess)

    def group_and_reduce_gradient(self, grad):
        grad_out = np.zeros(self.w.shape, dtype=np.float32)
        for i in range(self.N_clusters):
            cluster_mask = self.clusters_masks[i]
            centroid_grad = np.sum(grad * cluster_mask)

            grad_out = grad_out + cluster_mask * centroid_grad

        return grad_out

    # for numerical stability
    def quantize_centroids_update(self, sess):
        w_data = sess.run(self.w)
        for i in range(self.N_clusters):
            cluster_mask = self.clusters_masks[i]
            cluster_count = np.sum(cluster_mask)
            if cluster_count != 0:
                self.centroids[i] = np.sum(cluster_mask * w_data) / cluster_count
            else:  # do not modify
                pass

    # for numerical stability
    def quantize_weights_update(self, sess):
        w_data_updated = np.zeros(self.w.shape, dtype=np.float32)
        for i in range(self.N_clusters):
            cluster_mask = self.clusters_masks[i]
            centroid = self.centroids[i]

            w_data_updated = w_data_updated + cluster_mask * centroid
        sess.run(self.assign_w, feed_dict={self.w_PH: self.pruning_mask_data * w_data_updated})


class DenseLayer(object):
    def __init__(self, matrix, prune_mask, name, dense=False):
        assert matrix.shape == prune_mask.shape

        self.dense = dense
        self.N_in, self.N_out = matrix.shape

        if not self.dense:
            indices, values, dense_shape = [], [], [self.N_in, self.N_out]  # sparse matrix representation
            for i in range(self.N_in):
                for j in range(self.N_out):

                    # pruning mask: ones - valid weights, zero - pruned weights
                    if prune_mask[i][j] == 0.0:
                        continue

                    indices.append([i, j])
                    values.append(matrix[i][j])
            self.w_matrix = tf.SparseTensor(indices, values, dense_shape)  # tf sparse matrix
        else:
            self.w_matrix = tf.constant(matrix * prune_mask)  # tf dense matrix

    def forward(self, x):

        if not self.dense:
            w = tf.sparse.transpose(self.w_matrix, (1, 0))
            x = tf.transpose(x, (1, 0))
            x = tf.sparse.sparse_dense_matmul(w, x)  # only left matrix can be sparse hence transpositions
            x = tf.transpose(x, (1, 0))
        else:
            x = tf.matmul(x, self.w_matrix)
        return x


class ConvLayer(object):

    def __init__(self, tensor, prune_mask, H_in, W_in, stride, name, dense=False):

        assert tensor.shape == prune_mask.shape

        self.stride = stride
        self.dense = dense

        if self.dense == False:
            indices, values, dense_shape = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
            dense_shape[1] = int(round(dense_shape[1]))
            self.w_matrix = tf.SparseTensor(indices, values, dense_shape)  # tf sparse matrix

        else:
            matrix = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
            self.w_matrix = tf.constant(matrix)  # tf dense matrix

        self.w_tensor = tf.constant(tensor * prune_mask)

        print('layer:', name)
        print('\tvalid matrix weights:', int(np.sum(prune_mask)))
        print('\ttotal tensor weights:', np.product(self.w_tensor.shape))
        print('\ttotal matrix weights:', np.product(self.w_matrix.shape))

    def get_linear_pos(self, i, j, W):  # row major

        return i * W + j

    def tensor_to_matrix(self, tensor, prune_mask, H_in, W_in, stride):

        # assume padding type 'SAME' and padding value 0

        H_out = int(int(H_in + 1) / stride)  # padding 'SAME'
        W_out = int(int(W_in + 1) / stride)  # padding 'SAME'
        H_in = int(H_in)
        W_in = int(W_in)

        kH, kW, D_in, D_out = tensor.shape

        self.D_out = D_out
        self.H_out = H_out
        self.W_out = W_out

        if self.dense == False:
            indices, values, dense_shape = [], [], [H_in * W_in * D_in, H_out * W_out * D_out]  # sparse matrix
        else:
            matrix = np.zeros((H_in * W_in * D_in, H_out * W_out * D_out), dtype=np.float32)  # dense matrix

        for d_in in range(D_in):
            for d_out in range(D_out):

                # tf.nn.conv2d implementation doesn't go from top-left spatial location but from bottom-right
                for i_in_center in np.arange(H_in - 1, -1, -stride):  # kernel input center for first axis
                    for j_in_center in np.arange(W_in - 1, -1, -stride):  # kernel input center for second axis

                        i_out = int(i_in_center / stride)
                        j_out = int(j_in_center / stride)

                        for i in range(kH):

                            i_in = int(i_in_center + i - kH / 2)

                            if i_in < 0 or i_in >= H_in:  # padding value 0
                                continue

                            for j in range(kW):

                                j_in = int(j_in_center + j - kW / 2)

                                if j_in < 0 or j_in >= W_in:  # padding value 0
                                    continue

                                # pruning mask: ones - valid weights, zero - pruned weights
                                if prune_mask[i][j][d_in][d_out] == 0.0:
                                    continue

                                pos_in = int(self.get_linear_pos(i_in, j_in, W_in) + d_in * H_in * W_in)
                                pos_out = int(self.get_linear_pos(i_out, j_out, W_out) + d_out * H_out * W_out)

                                if self.dense == False:
                                    indices.append([pos_in, pos_out])
                                    values.append(tensor[i][j][d_in][d_out])
                                else:
                                    matrix[pos_in][pos_out] = tensor[i][j][d_in][d_out]

        if self.dense == False:
            return indices, values, dense_shape
        else:
            return matrix

    def forward_matmul_preprocess(self, x):

        x = tf.transpose(x, (0, 3, 1, 2))
        x = tf.reshape(x, (-1, np.product(x.shape[1:])))

        return x

    def forward_matmul_postprocess(self, x):

        x = tf.reshape(x, [-1, self.D_out, int(self.H_out), int(self.W_out)])
        x = tf.transpose(x, (0, 2, 3, 1))

        return x

    def forward_matmul(self, x):

        if self.dense == False:
            w = tf.sparse.transpose(self.w_matrix, (1, 0))
            x = tf.transpose(x, (1, 0))
            x = tf.sparse.sparse_dense_matmul(w, x)  # only left matrix can be sparse hence transpositions
            x = tf.transpose(x, (1, 0))
        else:
            x = tf.matmul(x, self.w_matrix)

        return x

    def forward_conv(self, x):

        return tf.nn.conv2d(x, self.w_tensor, strides=[1, self.stride, self.stride, 1], padding='SAME')


# class ConvLayer(object):
#     def __init__(self, tensor, prune_mask, H_in, W_in, stride, name, dense=False):
#         assert tensor.shape == prune_mask.shape
#
#         self.stride = stride
#         self.dense = dense
#
#         if not self.dense:
#             indices, values, dense_shape = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
#             # for i in range(len(indices)):
#             #     for j in range(0, 2):
#             #         indices[i][j] = int(np.round(indices[i][j]))
#             # for i in range(0, 2):
#             dense_shape[1] = int(round(dense_shape[1]))
#             #     dense_shape[i] = int(np.round(dense_shape[i]))
#             self.w_matrix = tf.SparseTensor(indices, values, dense_shape)  # tf sparse matrix
#         else:
#             matrix = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
#             self.w_matrix = tf.constant(matrix)  # tf dense matrix
#
#         self.w_tensor = tf.constant(tensor * prune_mask)
#
#     def get_linear_pos(self, i, j, W):  # row major
#         return i * W + j
#
#     def tensor_to_matrix(self, tensor, prune_mask, H_in, W_in, stride):
#         # assume padding type 'SAME' and padding value 0
#
#         global indices, values, matrix, dense_shape
#         H_out = int(H_in + 1) / stride  # padding 'SAME'
#         W_out = int(W_in + 1) / stride  # padding 'SAME'
#         H_in = int(H_in)
#         W_in = int(W_in)
#
#         kH, kW, D_in, D_out = tensor.shape
#
#         self.D_out = D_out
#         self.H_out = H_out
#         self.W_out = W_out
#
#         if not self.dense:
#             indices, values, dense_shape = [], [], [H_in * W_in * D_in, H_out* W_out * D_out] # sparse matrix
#         else:
#             matrix = np.zeros((H_in * W_in * D_in, H_out * W_out * D_out), dtype=np.float32)  # dense matrix
#
#         for d_in in range(D_in):
#             for d_out in range(D_out):
#                 # tf.nn.conv2d implementation doesn't go from top-left spatial location but from bottom-right
#                 for i_in_center in np.arange(H_in - 1, -1, -stride):  # kernel input center for first axis
#                     for j_in_center in np.arange(W_in - 1, -1, -stride):  # kernel input center for second axis
#                         i_out = int(i_in_center / stride)
#                         j_out = int(j_in_center / stride)
#                         for i in range(kH):
#                             i_in = i_in_center + i - kH / 2
#                             if i_in < 0 or i_in >= H_in:  # padding value 0
#                                 continue
#
#                             for j in range(kW):
#                                 j_in = j_in_center + j - kW / 2
#                                 if j_in < 0 or j_in >= W_in:  # padding value 0
#                                     continue
#                                 # pruning mask: ones - valid weights, zero - pruned weights
#                                 if prune_mask[i][j][d_in][d_out] == 0.0:
#                                     continue
#
#                                 pos_in = int(self.get_linear_pos(i_in, j_in, W_in) + d_in * H_in * W_in)
#                                 pos_out = int(self.get_linear_pos(i_out, j_out, W_out) + d_out * H_out * W_out)
#
#                                 if not self.dense:
#                                     indices.append([pos_in, pos_out])
#                                     values.append(tensor[i][j][d_in][d_out])
#                                 else:
#                                     matrix[pos_in][pos_out] = tensor[i][j][d_in][d_out]
#         if not self.dense:
#             return np.round(indices), values, dense_shape
#         else:
#             return matrix
#
#     def forward_matmul_preprocess(self, x):
#         x = tf.transpose(x, (0, 3, 1, 2))
#         x = tf.reshape(x, (-1, np.product(x.shape[1:])))
#
#         return x
#
#     def forward_matmul_postprocess(self, x):
#         x = tf.reshape(x, [-1, self.D_out, int(self.H_out), int(self.W_out)])
#         x = tf.transpose(x, (0, 2, 3, 1))
#
#         return x
#
#     def forward_matmul(self, x):
#         if not self.dense:
#             w = tf.sparse.transpose(self.w_matrix, (1, 0))
#             x = tf.transpose(x, (1, 0))
#             x = tf.sparse.sparse_dense_matmul(w, x)  # only left matrix can be sparse hence transpositions
#             x = tf.transpose(x, (1, 0))
#         else:
#             x = tf.matmul(x, self.w_matrix)
#
#         return x
#
#     def forward_conv(self, x):
#         return tf.nn.conv2d(x, self.w_tensor, strides=[1, self.stride, self.stride, 1], padding='SAME')


class NNModel:
    def __init__(self, problem: Problem, name, weights, prune_mask):
        self.problem = problem
        self.name = name
        self.weights = weights
        self.prune_mask = prune_mask

    def build_model(self, weights, prune_mask):
        x_PH = tv.v1.placeholder(tf.float32, [None, 28, 28, 1])

        model = Sequential()
        layer1 = model.add(ConvLayer(weights, prune_mask, x_PH.shape[1], x_PH.shape[2], 2, 'conv1'))
        x = model.add(layer1.forward_matmul_preprocess(x_PH))
        x = model.add(tf.nn.relu(layer1.forward_matmul(x)))
        x = model.add(layer1.forward_matmul_postprocess(x))

        layer2 = model.add(ConvLayer(weights, prune_mask, x.shape[1], x.shape[2], 2, 'conv2'))
        x = model.add(layer2.forward_matmul_preprocess(x))
        x = model.add(tf.nn.relu(layer2.forward_matmul(x)))
        x = model.add(layer2.forward_matmul_postprocess(x))

        x = tf.reshape(x, [-1, 7 * 7 * 64])

        layer3 = model.add(DenseLayer(weights, prune_mask, 'fc1'))
        x = model.add(tf.nn.relu(layer3.forward(x)))

        layer4 = model.add(DenseLayer(weights, prune_mask, 'fc2'))
        logits = model.add(layer4.forward(x))

        labels = tv.v1.placeholder(tf.float32, [None, 10])
        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        return model, accuracy


'''
    class for quantization of Optimizers
    
    url : https://arxiv.org/pdf/1711.00215.pdf
    paper: Minimum Energy Quantized Neural Networks
    
    url : https://arxiv.org/pdf/1602.02830.pdf
    paper: Binarized Neural Networks: Training Neural Networks with Weights and Activations Constrained to +1 or −1
'''


class Quantized_optimizers:

    def __init__(self):
        pass

    def round_opt(self, x):
        rounded = K.round(x)
        rounded_opt = x + K.stop_gradient(rounded - x)

        return rounded_opt

    def clip_opt(self, x, min, max):
        clipped = K.clip(x, min, max)
        return x + K.stop_gradient(clipped - x)

    def hard_sigmoid(self, x):
        result = K.clip((x + 1) / 2, 0, 1)
        return result

    def quantized_relu(self, W, nb=16):
        nb_bits = nb
        Wq = K.clip(2. * (Quantized_optimizers.round_opt(self, Quantized_optimizers.hard_sigmoid(self, W) *
                                                         pow(2, nb_bits)) / pow(2, nb_bits)) - 1., 0,
                    1 - 1.0 / pow(2, nb_bits - 1))
        return Wq

    def quantized_tanh(self, W, nb=16):
        non_sign_bits = nb - 1
        m = pow(2, non_sign_bits)
        Wq = K.clip(Quantized_optimizers.round_opt(self, W * m), -m, m - 1) / m

        return Wq

    def quantized_leakyrelu(self, W, nb=16, alpha=0.1):
        global negative_part
        if alpha != 0:
            negative_part = tf.nn.relu(-W)
        W = tf.nn.relu(W)
        if alpha != 0:
            alpha = tf.cast(tf.convert_to_tensor(alpha), W.dtype.base_dtype)
            W -= alpha * negative_part
        non_sign_bits = nb - 1
        m = pow(2, non_sign_bits)
        Wq = K.clip(Quantized_optimizers.round_opt(self, W * m), -m, m - 1) / m

        return Wq

    def quantize(self, W, nb=16, clip_through=False):
        non_sign_bits = nb - 1
        m = pow(2, non_sign_bits)
        if clip_through:
            Wq = self.clip_opt(Quantized_optimizers.round_opt(self ,W * m), -m, m - 1) / m
        else:
            Wq = K.clip(Quantized_optimizers.round_opt(self, W * m), -m, m - 1) / m

        return Wq

    def mean_abs(self, x, axis=None, keepdims=False):
        return K.stop_gradient(K.mean(K.abs(x), axis=axis, keepdims=keepdims))

    def Xnorize(self, W, H=1, axis=None, keepdims=False):
        Wb = self.quantize(W, H)
        Wa = self.mean_abs(W, axis, keepdims)


class Clip(constraints.Constraint):
    def __init__(self, min_value, max_value=None):
        self.min = min_value
        self.max = max_value
        if not self.max:
            self.max = -self.min
        if self.min > self.max:
            self.min = self.max
            self.max = self.min

    def __call__(self, p):
        return K.clip(p, self.min_value, self.max_value)


'''
    class for quantization of Dense Layer
    
    url : https://arxiv.org/pdf/1711.00215.pdf
    paper: Minimum Energy Quantized Neural Networks
    
    url : https://arxiv.org/pdf/1602.02830.pdf
    paper: Binarized Neural Networks: Training Neural Networks with Weights and Activations Constrained to +1 or −1
'''


class DenseQuantized(Dense):
    """
        Layer weight initializers : 'glorot_uniform'
        The neural network needs to start with some weights and then iteratively update them to better values.
        The term kernel_initializer is a fancy term for which statistical distribution or function to use for
        initialising the weights.
    """

    def __init__(self, units, H=1.0, nb=16, kernel_multiplier='glorot_uniform', bias_multiplier=None, **kwargs):
        super(DenseQuantized, self).__init__(units, **kwargs)
        self.H = H
        self.nb = nb
        self.kernel_multiplier = kernel_multiplier
        self.bias_multiplier = bias_multiplier
        super(DenseQuantized, self).__init__(units, **kwargs)

    def build(self, input_shape):
        input_dim = input_shape[1]
        if self.H == 'glorot_unifrom':
            self.H = np.float32(np.sqrt(1.5 / (input_dim + self.units)))
        if self.kernel_multiplier == 'glorot_uniform':
            self.kernel_multiplier = np.float32(1. / np.sqrt(1.5 / (input_dim + self.units)))

        self.kernel_constraint = Clip(-self.H, self.H)
        self.kernel_initializer = initializers.initializers_v1.RandomUniform(-self.H, self.H)
        self.kernel = self.add_weight(shape=(input_dim, self.units),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        if self.use_bias:
            self.lr_multipliers = [self.kernel_lr_multiplier, self.bias_lr_multiplier]
            self.bias = self.add_weight(shape=(self.units,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
        else:
            self.lr_multipliers = [self.kernel_multiplier]
            self.bias = None

        """
        Specifies the rank, dtype and shape of every input to a layer.

        Layers can expose (if appropriate) an `input_spec` attribute:
        an instance of `InputSpec`, or a nested structure of `InputSpec` instances
        (one per input tensor). These objects enable the layer to run input
        compatibility checks for input structure, input rank, input shape, and
        input dtype.

        A None entry in a shape is compatible with any dimension,
        a None shape is compatible with any shape.
        """
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True

    def call(self, inputs):
        quantized_kernel = Quantized_optimizers.quantize(self, self.kernel, nb=self.nb)
        output = K.dot(inputs, quantized_kernel)
        if self.use_bias:
            output = K.bias_add(output, self.bias)
        if self.activation is not None:
            output = self.activation(output)

        return output


'''
    class for quantization of Convolution Layer
    
    url : https://arxiv.org/pdf/1711.00215.pdf
    paper: Minimum Energy Quantized Neural Networks
    
    url : https://arxiv.org/pdf/1602.02830.pdf
    paper: Binarized Neural Networks: Training Neural Networks with Weights and Activations Constrained to +1 or −1.
'''


class ConvQuantized(Conv2D):
    """
        Layer weight initializers : 'glorot_uniform'
        The neural network needs to start with some weights and then iteratively update them to better values.
        The term kernel_initializer is a fancy term for which statistical distribution or function to use for
        initialising the weights.
    """

    def __init__(self, filters, kernel_regularizer=None, activity_regularizer=None, kernel_multiplier='glorot_uniform',
                 bias_multiplier=None, H=1.0, nb=16, **kwargs):
        super(ConvQuantized, self).__init__(filters, **kwargs)
        self.H = H
        self.nb = nb
        self.kernel_multiplier = kernel_multiplier
        self.bias_multiplier = bias_multiplier
        self.activity_regularizer = activity_regularizer
        self.kernel_regularizer = kernel_regularizer

    def build(self, input_shape):

        input_dim = input_shape[1]
        kernel_shape = self.kernel_size + (input_dim, self.filters)

        base = self.kernel_size[0] * self.kernel_size[1]
        if self.H == 'glorot_uniform':
            nb_input = int(input_dim * base)
            nb_output = int(self.filters * base)
            self.H = np.float32(np.sqrt(1.5 / (nb_input + nb_output)))

        if self.kernel_multiplier == 'glorot_uniform':
            nb_input = int(input_dim * base)
            nb_output = int(self.filters * base)
            self.kernel_multiplier = np.float32(1. / np.sqrt(1.5 / (nb_input + nb_output)))

        self.kernel_constraint = Clip(-self.H, self.H)
        self.kernel_initializer = initializers.RandomUniform(-self.H, self.H)
        self.kernel = self.add_weight(shape=kernel_shape,
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)

        if self.use_bias:
            self.lr_multipliers = [self.kernel_multiplier, self.bias_multiplier]
            self.bias = self.add_weight(shape=(self.filters,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)

        else:
            self.lr_multipliers = [self.kernel_multiplier]
            self.bias = None

        """
            Specifies the rank, dtype and shape of every input to a layer.

            Layers can expose (if appropriate) an `input_spec` attribute:
            an instance of `InputSpec`, or a nested structure of `InputSpec` instances
            (one per input tensor). These objects enable the layer to run input
            compatibility checks for input structure, input rank, input shape, and
            input dtype.

            A None entry in a shape is compatible with any dimension,
            a None shape is compatible with any shape.
        """
        self.input_spec = InputSpec(ndim=4, axes={1: input_dim})
        self.built = True

    def call(self, inputs):
        quantized_kernel = Quantized_optimizers.quantize(self, self.kernel, nb=self.nb)

        inverse_kernel_multiplier = 1. / self.kernel_multiplier
        inputs_qnn_gradient = (inputs - (1. - 1. / inverse_kernel_multiplier) * K.stop_gradient(inputs)) \
                              * inverse_kernel_multiplier

        outputs_qnn_gradient = K.conv2d(
            inputs_qnn_gradient,
            quantized_kernel,
            strides=self.strides,
            padding=self.padding,
            data_format=self.data_format,
            dilation_rate=self.dilation_rate)

        outputs = (outputs_qnn_gradient - (1. - 1. / self.kernel_lr_multiplier) *
                   K.stop_gradient(outputs_qnn_gradient)) * self.kernel_lr_multiplier

        if self.use_bias:
            outputs = K.bias_add(
                outputs,
                self.bias,
                data_format=self.data_format)

        if self.activation is not None:
            return self.activation(outputs)

        return outputs


# TODO: prepare the dataset and then implement this method
def load_dataset(dataset):
    # TODO: Move it to the import section.
    #  If you want to load your data, remove line below.
    from tensorflow.keras.datasets import cifar10, mnist
    from sklearn.model_selection import train_test_split
    x_train, y_train, x_test, y_test = cifar10.load_data()

    # TODO : for your own data, uncomment the line below, and comment line above.
    # x_train, y_train, x_test, y_test = train_test_split(dataset)

    return x_train, y_train, x_test, y_test


class QNN_model:
    def __init__(self, problem: Problem):
        self.problem = problem
        # self.x = x
        self.epochs = 100
        self.lr = 0.001   # Learning Rate
        self.decay = 0.000025

        # bits can be None, 2, 4, 8 , whatever
        self.bits = None
        self.wbits = 4
        self.abits = 4

        # width and depth
        self.nla, self.nlb, self.nlc = 1, 1, 1
        self.nfa, self.nfb, self.nfc = 64, 64, 64

        self.batch_size = 64

        # learning rate decay, factor => LR *= factor
        self.kernel_multiplier = 10
        self.decay_at_epoch = [0, 25, 80]
        self.factor_at_epoch = [1, 0.1, 1]

        self.channels = 3
        self.dim = 32
        # regularization
        self.kernel_regularizer = 0.0
        self.activity_regularizer = 0.0
        self.channels = 3
        self.progress_logging = 1
        # TODO: change dataset to my own data, and remove import line
        # dataframe_path = '/home/hamid/PycharmProjects/Artap/examples/Antenna/dataframe.txt'
        # self.dataframe = pd.read_csv(dataframe_path)
        # self.dataset = self.dataframe.values
        from tensorflow.keras.datasets import cifar10
        self.dataset = cifar10
        self.out_wght_path = '/home/hamid/PycharmProjects/Artap/examples/Antenna/weights.hdf5'

    def build_model(self, problem):
        H = 1

        Conv_ = lambda s, f, i, c: ConvQuantized(kernel_size=(s, s), H=1, nb=self.wbits, filters=f, strides=(1, 1),
                                                   padding='same', activation='linear',
                                                   kernel_regularizer=l2(self.kernel_regularizer),
                                                   kernel_multiplier=self.kernel_multiplier, input_shape=(i, i, c))
        Conv = lambda s, f: ConvQuantized(kernel_size=(s, s), H=1, nb=self.wbits, filters=f, strides=(1, 1),
                                            padding='same', activation='linear',
                                            kernel_regularizer=l2(self.kernel_regularizer),
                                            kernel_multiplier=self.kernel_multiplier)
        Act = lambda: Activation(Quantized_optimizers.quantized_relu)

        model = Sequential()
        model.add(Conv_(3, self.nfa, self.dim, self.channels))
        model.add(BatchNormalization(momentum=0.1, epsilon=0.0001))
        model.add(Act())

        """
        Each tested network contains 4 stages. 3 QNN-blocks, each followed by a max-pooling
        layer and 1 fully-connected classification stage. Each QNN-block is defined by 2 parameters: the
        number of basic building blocks n and the layer width F.
        Every QNN-sequence is a cascade of a QNN-layer, followed
        by a batch-normalization layer and a quantized activation
        function.
        """
        # block A
        for i in range(0, self.nla - 1):
            model.add(Conv(3, self.nfa))
            model.add(BatchNormalization(momentum=0.1, epsilon=0.0001))
            model.add(Act())
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # block B
        for i in range(0, self.nlb):
            model.add(Conv(3, self.nfb))
            model.add(BatchNormalization(momentum=0.1, epsilon=0.0001))
            model.add(Act())
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # block C
        for i in range(0, self.nlc):
            model.add(Conv(3, self.nfc))
            model.add(BatchNormalization(momentum=0.1, epsilon=0.0001))
            model.add(Act())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.summary()

        return model

    # learning rate schedule
    def scheduler(self, problem, model, epoch, x_train):
        if epoch in self.decay_at_epoch:
            index = self.decay_at_epoch.index(epoch)
            factor = self.factor_at_epoch[index]
            lr = K.get_value(model.optimizer.lr)

            # TODO: Add x_train to here.
            IT = x_train.shape[0] / self.batch_size
            current_lr = lr * (1. / (1. + self.decay * epoch * IT))
            K.set_value(model.optimizer.lr, current_lr * factor)

        return K.get_value(model.optimizer.lr)

    def train(self, problem):

        model = self.build_model(problem)
        early_stop = EarlyStopping(monitor='loss', min_delta=0.001, patience=10, mode='min', verbose=1)
        checkpoint = ModelCheckpoint(self.out_wght_path, monitor='val_acc', verbose=1, save_best_only=True,
                                     mode='max', period=1)

        # TODO: The line bellow must be added, first specify the dataset, and then implement load_dataset
        x_train, y_train, x_test, y_test = load_dataset(self.dataset)

        lr_decay = LearningRateScheduler(self.scheduler)
        adam = Adam(lr=problem.lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=self.decay)
        model.compile(loss=squared_hinge, optimizer=adam, metrics=['accuracy'])

        model.fit(x_train, y_train,
                  batch_size=self.batch_size,
                  epochs=self.epochs,
                  verbose=self.progress_logging,
                  callbacks=[checkpoint, lr_decay])
        # validation_data=(val_data.X, val_data.y))
