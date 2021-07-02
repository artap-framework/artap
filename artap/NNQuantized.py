import sys
from random import *
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import InputSpec, Layer, Dense, Conv2D
from keras import constraints
from keras import initializers

from .individual import Individual
from .problem import Problem
from .archive import Archive

'''
    paper: Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding.
    url : https://arxiv.org/abs/1510.00149
    The goal is to compress the neural network using weights quantization with no loss of accuracy.
'''


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

        if not self.dense:
            indices, values, dense_shape = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
            self.w_matrix = tf.SparseTensor(indices, values, dense_shape)  # tf sparse matrix
        else:
            matrix = self.tensor_to_matrix(tensor, prune_mask, H_in, W_in, stride)
            self.w_matrix = tf.constant(matrix)  # tf dense matrix

        self.w_tensor = tf.constant(tensor * prune_mask)

    def get_linear_pos(self, i, j, W):  # row major
        return i * W + j

    def tensor_to_matrix(self, tensor, prune_mask, H_in, W_in, stride):
        # assume padding type 'SAME' and padding value 0

        H_out = int(H_in + 1) / stride  # padding 'SAME'
        W_out = int(W_in + 1) / stride  # padding 'SAME'
        H_in = int(H_in)
        W_in = int(W_in)

        kH, kW, D_in, D_out = tensor.shape

        self.D_out = D_out
        self.H_out = H_out
        self.W_out = W_out

        if not self.dense:
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
                            i_in = i_in_center + i - kH / 2
                            if i_in < 0 or i_in >= H_in:  # padding value 0
                                continue

                            for j in range(kW):
                                j_in = j_in_center + j - kW / 2
                                if j_in < 0 or j_in >= W_in:  # padding value 0
                                    continue
                                # pruning mask: ones - valid weights, zero - pruned weights
                                # if prune_mask[i][j][d_in][d_out] == 0.0:
                                #     continue

                                pos_in = self.get_linear_pos(i_in, j_in, W_in) + d_in * H_in * W_in
                                pos_out = self.get_linear_pos(i_out, j_out, W_out) + d_out * H_out * W_out

                                if not self.dense:
                                    indices.append([pos_in, pos_out])
                                    values.append(tensor[i][j][d_in][d_out])
                                else:
                                    matrix[pos_in][pos_out] = tensor[i][j][d_in][d_out]
        if not self.dense:
            return indices, values, dense_shape
        else:
            return matrix

    def forward_matmul_preprocess(self, x):
        x = tf.transpose(x, (0, 3, 1, 2))
        x = tf.reshape(x, (-1, np.product(x.shape[1:])))

        return x

    def forward_matmul_postprocess(self, x):
        x = tf.reshape(x, (-1, self.D_out, self.H_out, self.W_out))
        x = tf.transpose(x, (0, 2, 3, 1))

        return x

    def forward_matmul(self, x):
        if not self.dense:
            w = tf.sparse.transpose(self.w_matrix, (1, 0))
            x = tf.transpose(x, (1, 0))
            x = tf.sparse.sparse_dense_matmul(w, x)  # only left matrix can be sparse hence transpositions
            x = tf.transpose(x, (1, 0))
        else:
            x = tf.matmul(x, self.w_matrix)

        return x

    def forward_conv(self, x):
        return tf.nn.conv2d(x, self.w_tensor, strides=[1, self.stride, self.stride, 1], padding='SAME')
