from method_bdf6 import BDF6Method
from rhs_function import ExampleFunc01
from rhs_function import ExampleFunc01_solution
from rhs_function import ExampleFunc02
from rhs_function import ExampleFunc02_solution
import numpy as np
import unittest


class TestBDF6Example(unittest.TestCase):

    def test_accuracy01(self):
        N = 10**3
        t = np.linspace(0, 1, num=N)
        # y0 = np.sin(np.linspace(-1.0*np.pi, 1.0*np.pi))
        y0 = np.array([np.pi])
        exactSol = ExampleFunc01_solution(y0, t).T

        # Compute numerical solution:
        bdf6_solver = BDF6Method(N, y0, [0, 1], ExampleFunc01())
        solution = bdf6_solver.generate()
        numericSol = np.zeros_like(exactSol)
        idx = 0
        for val in solution:
            numericSol[idx] = val[1]
            idx += 1

        err = np.max(np.abs(exactSol - numericSol))
        # BDF6 does not work correctly :/
        print("Error = {}".format(err))
        self.assertTrue(err < 10**(-12))

    def test_accuracy02(self):
        N = 2**10
        t = np.linspace(0, 1, num=N)
        y0 = np.array([1.0, 1.0]).T
        exactSol = ExampleFunc02_solution(y0, t)
        # Compute numerical solution:
        solver = BDF6Method(N, y0, [0, 1], ExampleFunc02())
        solution = solver.generate()
        numericSol = []
        for (time, val) in solution:
            numericSol.append(val)

        numericSol = np.array(numericSol).T
        err = np.max(np.abs(exactSol - numericSol))
        self.assertTrue(err < 5.0*10**(-13))

    def test_convergence_rate(self):
        N_arr = [2**n for n in range(1, 8)]

        def computeErr(N):
            """TODO: Docstring for computeErr.

            :N: Number of gridpoints
            :returns: err in inf norm

            """
            t = np.linspace(0, 1, num=N)
            # y0 = np.sin(np.linspace(-1.0*np.pi, 1.0*np.pi))
            y0 = np.array([np.pi])
            exactSol = ExampleFunc01_solution(y0, t).T

            # Compute numerical solution:
            bdf6_solver = BDF6Method(N, y0, [0, 1], ExampleFunc01())
            solution = bdf6_solver.generate()
            numericSol = np.zeros_like(exactSol)
            idx = 0
            for val in solution:
                numericSol[idx] = val[1]
                idx += 1

            err = np.max(np.abs(exactSol - numericSol))
            return err


        Err_arr = []
        for N in N_arr:
            err = computeErr(N)
            Err_arr.append(err)

        isOkay = True
        for Nidx in range(1, len(N_arr)):
            quotient = Err_arr[Nidx-1] / Err_arr[Nidx]
            print(Err_arr[Nidx], quotient)
            # I am using RK4 to initialise the method.
            # Can not expect anything higher than order 4
            if(quotient < 0.9*(2**4)):
                # We expect implicit euler to have second order here becuase
                # f'' = 0
                isOkay = False
        # Is okay contains if all improvemnts match up with expectations
        self.assertTrue(isOkay)


if __name__ == "__main__":
    unittest.main()
