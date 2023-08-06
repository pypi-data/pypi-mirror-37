from method_midpointrule import MidPointRule
from rhs_function import ExampleFunc01
from rhs_function import ExampleFunc01_solution
from rhs_function import ExampleFunc02
from rhs_function import ExampleFunc02_solution
import numpy as np
import unittest

class TestMidPointRule(unittest.TestCase):

    def test_accuracy01(self):
        N = 2**10
        t = np.linspace(0, 1, num=N)
        y0 = np.array([np.pi])
        exactSol = ExampleFunc01_solution(y0, t).T

        #  Compute numerical sol:
        mpr_solver = MidPointRule(N, y0, [0, 1], ExampleFunc01())
        solution = mpr_solver.generate()
        numericSol = np.zeros_like(exactSol)
        idx = 0
        for (time, val) in solution:
            numericSol[idx] = val
            idx += 1

        err = np.max(np.abs(exactSol-numericSol))
        print(err)
        self.assertTrue(err < 4.0*10**(-7))

    def test_accuracy02(self):
        N = 2**10
        t = np.linspace(0, 1, num=N)
        y0 = np.array([1.0, 1.0]).T
        exactSol = ExampleFunc02_solution(y0, t)
        # Compute numerical solution:
        solver = MidPointRule(N, y0, [0, 1], ExampleFunc02())
        solution = solver.generate()
        numericSol = []
        for (time, val) in solution:
            numericSol.append(val)

        numericSol = np.array(numericSol).T
        err = np.max(np.abs(exactSol - numericSol))
        print(err)
        self.assertTrue(err < 1.2*10**(-7))

    def test_convergence_rate(self):
        N_arr = [2**n for n in range(5, 11)]

        def computeErr(N):
            """TODO: Docstring for computeErr.

            :N: Number of gridpoints
            :returns: err in inf norm

            """
            t = np.linspace(0, 1, num=N)
            # y0 = np.sin(np.linspace(-1.0*np.pi, 1.0*np.pi))
            y0 = [np.pi]
            exactSol = ExampleFunc01_solution(y0, t).T
            # Compute numerical solution:
            mpr_solver = MidPointRule(N, y0, [0, 1], ExampleFunc01())
            solution = mpr_solver.generate()
            numericSol = np.zeros_like(exactSol)
            idx = 0
            for (time, val) in solution:
                numericSol[idx] = val
                idx += 1

            err = np.max(np.abs(exactSol - numericSol))
            return err

        Err_arr = []
        for Nidx in range(len(N_arr)):
            N = N_arr[Nidx]
            err = computeErr(N)
            Err_arr.append(err)

        isOkay = True
        for Nidx in range(1, len(N_arr)):
            quotient = Err_arr[Nidx-1] / Err_arr[Nidx]
            # Test if the improvement is in 10% of the expected value
            if(quotient < 3.6):
                isOkay = False
        # Is okay contains if all improvemnts match up with expectations
        self.assertTrue(isOkay)

if __name__ == "__main__":
    unittest.main()
