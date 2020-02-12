import time
import nlopt

from .problem import Problem
from .algorithm import Algorithm
from .job import JobSimple

GN_DIRECT = nlopt.GN_DIRECT
GN_DIRECT_L = nlopt.GN_DIRECT_L
GN_DIRECT_L_RAND = nlopt.GN_DIRECT_L_RAND
GN_DIRECT_NOSCAL = nlopt.GN_DIRECT_NOSCAL
GN_DIRECT_L_NOSCAL = nlopt.GN_DIRECT_L_NOSCAL
GN_DIRECT_L_RAND_NOSCAL = nlopt.GN_DIRECT_L_RAND_NOSCAL
GN_ORIG_DIRECT = nlopt.GN_ORIG_DIRECT
GN_ORIG_DIRECT_L = nlopt.GN_ORIG_DIRECT_L
GD_STOGO = nlopt.GD_STOGO
GD_STOGO_RAND = nlopt.GD_STOGO_RAND
LD_LBFGS_NOCEDAL = nlopt.LD_LBFGS_NOCEDAL
LD_LBFGS = nlopt.LD_LBFGS
LN_PRAXIS = nlopt.LN_PRAXIS
LD_VAR1 = nlopt.LD_VAR1
LD_VAR2 = nlopt.LD_VAR2
LD_TNEWTON = nlopt.LD_TNEWTON
LD_TNEWTON_RESTART = nlopt.LD_TNEWTON_RESTART
LD_TNEWTON_PRECOND = nlopt.LD_TNEWTON_PRECOND
LD_TNEWTON_PRECOND_RESTART = nlopt.LD_TNEWTON_PRECOND_RESTART
GN_CRS2_LM = nlopt.GN_CRS2_LM
GN_MLSL = nlopt.GN_MLSL
GD_MLSL = nlopt.GD_MLSL
GN_MLSL_LDS = nlopt.GN_MLSL_LDS
GD_MLSL_LDS = nlopt.GD_MLSL_LDS
LD_MMA = nlopt.LD_MMA
LN_COBYLA = nlopt.LN_COBYLA
LN_NEWUOA = nlopt.LN_NEWUOA
LN_NEWUOA_BOUND = nlopt.LN_NEWUOA_BOUND
LN_NELDERMEAD = nlopt.LN_NELDERMEAD
LN_SBPLX = nlopt.LN_SBPLX
LN_AUGLAG = nlopt.LN_AUGLAG
LD_AUGLAG = nlopt.LD_AUGLAG
LN_AUGLAG_EQ = nlopt.LN_AUGLAG_EQ
LD_AUGLAG_EQ = nlopt.LD_AUGLAG_EQ
LN_BOBYQA = nlopt.LN_BOBYQA
GN_ISRES = nlopt.GN_ISRES
AUGLAG = nlopt.AUGLAG
AUGLAG_EQ = nlopt.AUGLAG_EQ
G_MLSL = nlopt.G_MLSL
G_MLSL_LDS = nlopt.G_MLSL_LDS
LD_SLSQP = nlopt.LD_SLSQP
LD_CCSAQ = nlopt.LD_CCSAQ
GN_ESCH = nlopt.GN_ESCH
GN_AGS = nlopt.GN_AGS

_algorithm = [nlopt.GN_DIRECT_L, GN_DIRECT_L_RAND, GN_MLSL, GN_CRS2_LM, GN_ISRES, GN_ESCH, LN_BOBYQA, LN_COBYLA, LN_NELDERMEAD, LN_SBPLX,  LN_PRAXIS, LN_AUGLAG_EQ]

class NLopt(Algorithm):
    """ NLopt algorithms """

    def __init__(self, problem: Problem, name="NLopt"):
        super().__init__(problem, name)

        self.job = JobSimple(self.problem)
        self.options.declare(name='algorithm', default=LN_BOBYQA, values=_algorithm,
                             desc='Algorithm')
        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='xtol_rel', default=1e-6, lower=0.0,
                             desc='xtol_rel')
        self.options.declare(name='xtol_abs', default=1e-12, lower=0.0,
                             desc='xtol_abs')
        self.options.declare(name='ftol_rel', default=1e-6, lower=0.0,
                             desc='ftol_rel')
        self.options.declare(name='ftol_abs', default=1e-12, lower=0.0,
                             desc='ftol_abs')

    def _function(self, x, grad):
        return self.job.evaluate_scalar(x)

    def _constraint(x, grad, a, b):
        # if grad.size > 0:
        #     grad[0] = 3 * a * (a * x[0] + b) ** 2
        #     grad[1] = -1.0
        # return (a * x[0] + b) ** 3 - x[1]
        return 0

    def run(self):
        # Figure out bounds vectors.
        lb = []
        ub = []
        for parameter in self.problem.parameters:
            bounds = parameter['bounds']

            lb.append(bounds[0])
            ub.append(bounds[1])

        op = nlopt.opt(self.options['algorithm'], len(self.problem.parameters))
        op.set_lower_bounds(lb)
        op.set_upper_bounds(ub)
        op.set_min_objective(self._function)
        op.set_xtol_rel(self.options['xtol_rel'])
        op.set_xtol_abs(self.options['xtol_abs'])
        op.set_ftol_rel(self.options['ftol_rel'])
        op.set_ftol_abs(self.options['ftol_abs'])
        op.set_maxeval(self.options['n_iterations'])

        # constraint
        # op.add_inequality_constraint(lambda x, grad: myconstraint(x, grad, 2, 0), 1e-8)
        # op.add_inequality_constraint(lambda x, grad: myconstraint(x, grad, -1, 1), 1e-8)

        try:
            t_s = time.time()
            self.problem.logger.info("NLopt: {}".format(op.get_algorithm_name()))
            x = op.optimize(self.problem.get_initial_values())
            # print('initial values:',x)
            t = time.time() - t_s
            self.problem.logger.info("NLopt: elapsed time: {} s".format(t))

            """
            if self.options['verbose_level'] >= 1:
                print('method: ', op.get_algorithm_name())
                print('optimum at ', x)
                print('minimum value = ', op.last_optimum_value())
                print('nevals = ', op.get_numevals())
            """
        except RuntimeError:
            print('Optimization FAILED.')
            print(op.get_errmsg())
        except ValueError:
            print('Optimization FAILED.')
            print(op.get_errmsg())

        msg_nlopt = {-1: 'failure - generic failure code',
                     -2: 'failure - invalid arguments',
                     -3: 'failure - out of memory',
                     -4: 'failure - round off limited',
                     -5: 'failure - forced stop',
                      1: 'success - generic success code',
                      2: 'success - stop value reached',
                      3: 'success - ftol reached',
                      4: 'success - xtol reached',
                      5: 'success - maxeval reached',
                      6: 'success - maxtime reached'
                     }

        if self.options['verbose_level'] >= 1:
            print('optimum = ', op.last_optimum_value())
            print('result code and meaning = ', op.last_optimize_result(), msg_nlopt[op.last_optimize_result()])