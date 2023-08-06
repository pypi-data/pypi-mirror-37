from method_explicit_euler import ExplicitEuler
from rhs_function import RHSFunction
from scipy import optimize
from step_method import StepMethod
import numpy as np
import scipy.sparse as sparse


class ImplicitEuler(StepMethod):

    """This Class implements the implicit Euler time step method
       for solving ode problems."""

    def __init__(self, N, y0, domain, func):
        StepMethod.__init__(self, N, y0, domain, func)

    def step(self, f, u, t, h, tol=10**(-10), maxiter=10):
        t_new = t + h
        t_old = t
        # Create a copy of u
        y_old = np.copy(u)
        # Guess the new y_new using explicit Euler method
        y_new = y_old + h * f.eval(y_old, t_old)
        N = len(u)

        # Compute the function required for Newton iteration.
        def myF(y_new):
            val = y_new - y_old
            val = val - 0.5 * h * (f.eval(y_new, t_new) + f.eval(y_old, t_old))
            return val

        def myJacF(y_new):
            val1 = sparse.eye(N)
            val2 = -1.0 * (h/2) * f.jacobian(y_new, t_new)
            csrMtx = sparse.csr_matrix(val1 + val2)
            return csrMtx

        itercount = 0
        err = 1
        while err > tol and itercount < maxiter:
            Jac = myJacF(y_new)
            Fval = myF(y_new)
            y_update = sparse.linalg.spsolve(Jac, Fval)
            y_new = y_new - y_update
            itercount += 1
            err = np.max(np.abs(myF(y_new)))
        return y_new
