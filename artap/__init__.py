# from .algorithm import *
# from .executor import *
# from .algorithm_scipy import *
# from .algorithm_genetic import *

# import platform
#
# __agros__ = True
#
# try:
#     from agrossuite import agros as a2d
#
# except ImportError:
#     __agros__ = False
#
# try:
#     from .algorithm_bayesopt import *_
# except ImportError:
#     __bayes_opt__ = False
#
# try:
#     from .algorithm_nlopt import *_
# except ImportError:
#     __nl_opt__ = False
#
# # TODO: test if local Comsol is present
#
# # TODO: Repare
# if platform.system() == 'Linux':
#     from .algorithm_bayesopt import *
#
#     __all__ = ['Problem', 'NSGA_II', 'BayesOpt']
#
# else:
#     __all__ = ['Problem', 'NSGA_II']
# __all__ = ['Problem', 'NSGA_II']