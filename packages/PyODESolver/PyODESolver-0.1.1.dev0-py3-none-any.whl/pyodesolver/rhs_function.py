import scipy.sparse as sparse
import numpy as np


class RHSFunction(object):

    """Docstring for RHSFunction. """

    def __init__(self):
        pass

    def eval(self, y_vec, time):
        """TODO: Docstring for eval.

        :y_vec: The vector of the current y value
        :time: The time as double
        :returns: The evaluation f(y_vec, time)

        """
        raise NotImplementedError

    def jacobian(self, y_vec, time):
        """TODO: Docstring for jacobian.

        :y_vec: The vector of the current y value
        :time: The time as double
        :returns: The evaluation of the jacobina grad_y f(y_vec, time)

        """
        raise NotImplementedError

    def isLinear(self):
        raise NotImplementedError

class ExampleFunc01(RHSFunction):

    """Docstring for ExampleFunc01. """

    def __init__(self):
        """TODO: to be defined1. """
        RHSFunction.__init__(self)

    def eval(self, y_vec, time):
        """TODO: Docstring for eval.

        :y_vec: The vector of the current y value
        :time: The time as double
        :returns: The evaluation f(y_vec, time)

        """
        eval_vec = -2.0 * y_vec
        return eval_vec

    def jacobian(self, y_vec, time):
        """TODO: Docstring for jacobian.

        :y_vec: The vector of the current y value
        :time: The time as double
        :returns: The evaluation f(y_vec, time)

        """
        N = len(y_vec)
        jac = sparse.diags([-2.0], [0], shape=(N, N))
        return jac

    def isLinear(self):
        """ Returns weather this function is linear. Spoiler alert...
        It is :)

        :returns: True
        """
        return True

def ExampleFunc01_solution(y_0, t):
    """
    Evaluates the analytic solution to the the RHS_function
    ExampleFunc01. The purpose of this method is to provide
    a flexible testing environment.

    :y_0: The initial data
    :t: The time value. Passing an array is valid.
    :returns: The solution as a list

    """

    val1 = y_0
    val2 = np.exp(-2.0*t)
    res = np.outer(val1, val2)
    return res

class ExampleFunc02(RHSFunction):

    def __init__(self):
        RHSFunction.__init__(self)

    def eval(self, y_vec, time):
        val1 = -y_vec[0]**2*y_vec[1]
        val2 = -y_vec[1]**2
        val3 = np.array([val1, val2])
        return val3

    def jacobian(self, y_vec, time):
        # fixed size of 2
        J11 = -2*y_vec[0]*y_vec[1]
        J12 = -y_vec[0]**2
        J21 = 0
        J22 = -2*y_vec[1]
        J = np.array([[J11, J12], [J21, J22]])
        return J


def ExampleFunc02_solution(y_0, t):
    val01 = 1/(np.log(1+t)+1)
    val02 = 1/(1+t)
    val03 = np.array([val01, val02])
    return val03




















