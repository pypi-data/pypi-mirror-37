from method_Gauss_Legendre_2 import GaussLegendre
from rhs_function import ExampleFunc01
from rhs_function import ExampleFunc01_solution
import numpy as np
import unittest
import time as timedomain

class TestGaussLegendre(unittest.TestCase):

        def test_accuracy01(self):
            N=2**10
            t=np.linspace(0,1,num=N)
            y0=np.array([np.pi])
            exactSol = ExampleFunc01_solution(y0,t).T

            #  Compute Numerical Solution:
            t1=timedomain.time()
            GaussLegendre_solver=GaussLegendre(N, y0, [0,1],ExampleFunc01())
            solution= GaussLegendre_solver.generate()
            numericSol= np.zeros_like(exactSol)
            idx = 0
            for (time,val) in solution:
                    numericSol[idx] = val
                    idx += 1
            t2=timedomain.time()
            print(t2-t1)
            err=np.max(np.abs(exactSol-numericSol))
#            for i in range(N):
#               print(np.abs(exactSol[i]-numericSol[i]))
            self.assertTrue(err<4*10**(-7))


        def test_convergence_rate(self):
            N_arr = np.array([2**n for n in range(5, 11)])
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
                GL_solver = GaussLegendre(N, y0, [0, 1], ExampleFunc01())
                solution = GL_solver.generate()
                numericSol = np.zeros_like(exactSol)
                idx = 0
                for (time, val) in solution:
                    numericSol[idx] = val
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
#                print(quotient)
#                print(Err_arr[Nidx-1])
                if(quotient < 3.7):
                    # We expect implicit euler to have second order here becuase
                    # f'' = 0
                    isOkay = False
            # Is okay contains if all improvemnts match up with expectations
            self.assertTrue(isOkay)
if __name__ == "__main__":
    unittest.main()
