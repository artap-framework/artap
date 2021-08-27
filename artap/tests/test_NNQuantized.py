import unittest
import numpy as np
import tensorflow as tf
from ..NNQuantized import ConvLayer, DenseLayer
import tensorflow._api.v2.compat as tv
tv.v1.disable_v2_behavior()


class test_NNQuantize(unittest.TestCase):
    def test_ConvLayer(self):
        weights = np.random.uniform(-10.0, 10.0, size=(3, 3, 4, 5)).astype(np.float32)
        prune_mask = np.random.uniform(0.0, 2.0, size=(3, 3, 4, 5)).astype(np.int32).astype(np.float32)

        x = np.random.uniform(0.0, 1.0, size=(2, 14, 14, 4)).astype(np.float32)
        x = tf.constant(x)

        L = ConvLayer(weights, prune_mask, 14, 14, 2, 'conv')

        x_matmul_sparse = L.forward_matmul_preprocess(x)
        y_matmul_sparse = L.forward_matmul(x_matmul_sparse)
        y_matmul_sparse = L.forward_matmul_postprocess(y_matmul_sparse)

        y_conv = L.forward_conv(x)

        sess = tv.v1.Session()
        y_matmul_sparse_data, y_conv_data = sess.run([y_matmul_sparse, y_conv])
        s = np.mean(np.abs(y_matmul_sparse_data - y_conv_data))
        assert s > 1e-6

    def test_FcLayerDeploy(self):
        weights = np.random.uniform(-10.0, 10.0, size=(5, 10)).astype(np.float32)
        prune_mask = np.random.uniform(0.0, 2.0, size=(5, 10)).astype(np.int32).astype(np.float32)

        x = np.random.uniform(0.0, 1.0, size=(2, 5)).astype(np.float32)
        x = tf.constant(x)

        L_sparse = DenseLayer(weights, prune_mask, 'fc')
        L_dense = DenseLayer(weights, prune_mask, 'fc', dense=True)

        y_sparse = L_sparse.forward(x)
        y_dense = L_dense.forward(x)

        sess = tv.v1.Session()
        y_sparse_data, y_dense_data = sess.run([y_sparse, y_dense])
        s = np.mean(np.abs(y_sparse_data - y_dense_data))
        assert s < 1e-6