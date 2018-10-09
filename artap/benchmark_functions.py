# TODO: Add descriptions to benchmark functions


class Rosenbrock:

    @classmethod
    def eval(cls, X):
        # -30 <= xi <= 30
        # global minimal is at [1,1,..] where value = 0

        x = X[0]
        y = X[1]
        a = 1. - x
        b = y - x * x

        return [a * a + b * b * 100.0]


class Binh_and_Korn:

    @classmethod
    def eval(cls, x_list):
        # 0 <= x <=5, 0 <= y <= 3
        x = x_list[0]
        y = x_list[1]
        f1 = 4 * pow(x, 2) + 4 * pow(y, 2)
        f2 = pow(x - 5, 2) + pow(y - 5, 2)
        target = [f1, f2]
        return target

    @classmethod
    def constraints(cls, x_list):
        # 0 <= x <=5, 0 <= y <= 3
        x = x_list[0]
        y = x_list[1]
        g1 = max(0, 25 - pow(x - 5, 2) - pow(y, 2))
        g2 = max(0, pow(x - 8, 2) + pow(y + 3, 2) - 7.7)
        violation = [g1, g2]
        return violation
