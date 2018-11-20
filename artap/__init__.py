from .algorithm import *
from .executor import *
from .algorithm_scipy import *
from .algorithm_genetic import *

import platform

if platform.system() == 'Linux':
    from .algorithm_bayesopt import *

    __all__ = ['Problem', 'NSGA_II', 'BayesOpt']

else:
    __all__ = ['Problem', 'NSGA_II']
__all__ = ['Problem', 'NSGA_II']