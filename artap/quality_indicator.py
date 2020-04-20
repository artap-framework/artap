from scipy import spatial
import numpy as np

"""
Contains different quality indicators to benchmark the multi-objective optimization algorithms.

Indicators:

    - Generational Distance
    - Additive unary epsilon indicator
"""


def gd(reference: list, computed: list, norm='euclidean'):
    """
    :param reference: list of the reference points [(coord_1, coord_2, coord_3,..., coord_n)]
    :return: the sum of the euclidean disctance from the given reference points.

    Possible norms:  ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’,
                     ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulsinski’, ‘mahalanobis’, ‘matching’,
                     ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’,
                     ‘sqeuclidean’, ‘wminkowski’, ‘yule’.

    Type: Convergence Indicator

    The generational distance performence indicator [1,2,3] measueres the distancee from the
    given reference list. T

    .. math::

        GD(S,P) = \frac{1}{n}(\Sigma_{s \in S} min ||F(s) - F(r)||^2)^{\frac{1}{p}}

    where |S| is the number of the points in a Pareto-set approximation and P a discrete representation
    of the Pareto-front. Generally, p=2. In this case it is equivalent with M1 measure [4].
    When P = 1 it is equivalent with the Gamma-Metric.

    References
    ----------

    .: [1] David A. Van Veldhuizen and David A. Van Veldhuizen.
           Multi-objective evolutionary algorithms: classifications, analyses, and new innovations.
           Technical Report, Evolutionary Computation, 1999.
    .: [2] Audet, Charles, J. Bigeon, D. Cartier, Sébastien Le Digabel, and Ludovic Salomon.
           "Performance indicators in multiobjective optimization." Optimization Online (2018).
    .: [3] https://pymoo.org/misc/performance_indicator.html
    .: [4] E. Zitzler, K. Deb, L. Thiele, Comparison of multiobjective evolutionary algorithms: Empirical
           results, Evolutionary computation 8 (2) (2000) 173–195.

    """

    distances = spatial.distance.cdist(reference, computed, metric=norm)
    minimums = np.nanmin(distances, axis=0)

    return np.sum(minimums) / len(computed)


def epsilon_add(reference: list, computed: list):
    """
     :param reference: list of reference pareto-front values, list of tuples
     :param computed: list of the computed pareto-front values, list of tuples
     :return: additive unary epsilon indicator

     .. math::
        I_{\epsilon}(A,B) = max_{x^2 \in B} min_{x^1 \in A} max_{1 \leq i \leq m} f_i(x^1) - f_i(x^2)

     [1] E. Zitzler, E. Thiele, L. Laummanns, M., Fonseca, C., and Grunert da Fonseca. V (2003):
        Performance Assessment of Multiobjective Optimizers: An Analysis and
        Review. The code is the a Java version of the original metric implementation by Eckart Zitzler.

     [2] Audet, Charles, J. Bigeon, D. Cartier, Sébastien Le Digabel, and Ludovic Salomon.
         "Performance indicators in multiobjective optimization." Optimization Online (2018).
    """

    eps = 0.0
    for ref_val in reference:
        eps_j = np.infty
        for comp_val in computed:
            eps_k = max(np.subtract(comp_val, ref_val))
            eps_j = min(eps_k, eps_j)
        eps = max(eps, eps_j)

    return eps

