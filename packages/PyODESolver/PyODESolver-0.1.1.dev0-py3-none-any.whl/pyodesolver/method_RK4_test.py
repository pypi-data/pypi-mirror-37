import numpy as np
import matplotlib.pyplot as plt
import unittest
from method_RK4 import RK4
from rhs_function import ExampleFunc01
from rhs_function import ExampleFunc01_solution

class TestRK4(unittest.TestCase):

        def test_accuracy01(self):
            N = 10**3
            t = np.linspace(0, 1, num=N)
            y0 = np.array([np.pi])
            exactSol = ExampleFunc01_solution(y0, t).T

            #  Compute numerical solution:
            RK4_solver = RK4(N, y0, [0, 1], ExampleFunc01())
            solution = RK4_solver.generate()
            numericSol = np.zeros_like(exactSol)
            idx = 0
            for (time, val) in solution:
                numericSol[idx] = val
                idx += 1

            err = np.max(np.abs(exactSol-numericSol))
            print(err)
            self.assertTrue(err < 4.0*10**(-7))

        def test_convergence01(self):
            Narr = [2**n for n in range(3, 12)]
            err = []
            for N in Narr:
                t = np.linspace(0, 1, num=N)
                y0 = np.array([np.pi])
                exactSol = ExampleFunc01_solution(y0, t).T
                #  Compute numerical solution:
                RK4_solver = RK4(N, y0, [0, 1], ExampleFunc01())
                solution = RK4_solver.generate()
                numericSol = np.zeros_like(exactSol)
                idx = 0
                for (time, val) in solution:
                    numericSol[idx] = val
                    idx += 1

                err.append(np.max(np.abs(exactSol-numericSol)))

            isOkay = True
            ratio = []
            for i in range(1, len(err)):
                ratio.append((err[i-1] / err[i]))
                if ratio[i - 1] < 0.9*(2**4):
                    isOkay = False
                print((ratio[i-1], err[i]))
            self.assertTrue(isOkay)


if __name__ == "__main__":
    unittest.main()
