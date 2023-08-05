from scipy import optimize
from step_method import StepMethod
from method_RK4 import RK4
import numpy as np
import scipy.sparse as sparse


class BDF6Method(StepMethod):

    past_data = []
    starterMethod = None
    starterSolver = None

    def __init__(self, N, y0, domain, func):
        StepMethod.__init__(self, N, y0, domain, func)

        self.past_data = []
        # Start appending data to past data
        t0, tend = domain
        self.past_data.append(y0)

        # Define RK4 as the starter method:
        self.starterMethod = RK4(N, y0, domain, func)
        self.starterSolver = self.starterMethod.generate()
        next(self.starterSolver)

    def step(self, f, u, t, h, tol=10**(-12), maxiter=10):
        """Implements the step method for the BDF6 method
        :returns: generator for the step values
        """

        # For BDF6 to work we need 6 pieces of old data.
        # figure out if the past data is filled well:
        if(len(self.past_data) >= 6):
            # Implementation of the BDF6 method
            # Guess the y_new using RK4
            t_new = t + h
            y_new = np.copy(u) + h * f.eval(u, t)
            N = len(u)

            # define internal functions for the newton method:
            def myF(y):
                val = np.copy(y)
                val -= (360.0 / 147.0) * (self.past_data[-1])
                val += (450.0 / 147.0) * (self.past_data[-2])
                val -= (400.0 / 147.0) * (self.past_data[-3])
                val += (225.0 / 147.0) * (self.past_data[-4])
                val -= (72.0 / 147.0) * (self.past_data[-5])
                val += (10.0 / 147.0) * (self.past_data[-6])
                val -= h * (60.0 / 147.0) * f.eval(np.copy(y), t_new)
                return val

            # define the internal Jacobian for the newton method:
            def myJacF(y):
                val1 = sparse.eye(N)
                val2 = (60.0 / 147.0) * h * f.jacobian(np.copy(y), t_new)
                return sparse.csr_matrix(val1 - val2)

            itercount = 0
            err = 1
            while err > tol and itercount < maxiter:
                Jac = myJacF(y_new)
                Fval = myF(y_new)
                y_update = sparse.linalg.spsolve(Jac, Fval)
                y_new = y_new - y_update
                itercount += 1
                err = np.max(np.abs(myF(y_new)))
                # Err is always machine precision
            # Append to the list of past solutions:

        else:
            # Use RK4 for the first 6 timesteps:
            y_value = next(self.starterSolver)
            y_new = np.copy(y_value[1])

        # remove first value from array:
        self.past_data.append(y_new)

        return y_new
