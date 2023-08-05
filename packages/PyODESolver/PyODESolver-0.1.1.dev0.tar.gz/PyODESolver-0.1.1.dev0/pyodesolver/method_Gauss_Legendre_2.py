from rhs_function import RHSFunction
from scipy import optimize
import scipy.sparse as sparse
from scipy import optimize
from step_method import StepMethod
import numpy as np
class GaussLegendre(StepMethod):

        """
            This Class implements Gauss Legendre RK method for solving ODE
        """


        def __init__ (self,N,y0,domain,func):
            StepMethod.__init__(self, N, y0, domain, func)
            self.a11=0.25
            self.a12=0.25-np.sqrt(3)/6
            self.a21=0.25+np.sqrt(3)/6
            self.a22=0.25
            self.b1=0.5
            self.b2=0.5
            self.c1=0.5-np.sqrt(3)/6
            self.c2=0.5+np.sqrt(3)/6

        def step(self,f,u, t, h ,tol =  10**(-12), maxiter = 10):
            t_old= t
            #  Copy u
            y_old=np.copy(u)
            #  Guess k1 and k2
            k1 = f.eval(y_old,t_old)
            k2 = f.eval(y_old,t_old)
            N1=len(k1)
            def myF(k1,k2):
                val1 =np.vstack((k1, k2))
                val2 = h*(self.a11*k1+self.a12*k2)
                val3 = h*(self.a21*k1+self.a22*k2)
                f1=f.eval(y_old + val2, t_old+self.c1*h)
                f2=f.eval(y_old + val3, t_old+self.c2*h)
                val4 = np.vstack((f1, f2))
                return val4.flatten()-val1.flatten()

            def myJacF(k1,k2):
                val2 = h*(self.a11*k1 + self.a12*k2)
                val3 = h*(self.a21*k1 + self.a22*k2)

                A = f.jacobian(y_old+val2, t_old+self.c1*h)*self.a11*h
                B = A/self.a11*self.a12
                C = f.jacobian(y_old+val3, t_old+self.c2*h)*self.a21*h
                D = C/self.a21*self.a22
                E = np.vstack((A.T, B.T))
                F = np.vstack((C.T, D.T))
                G = np.vstack((E.T, F.T))
                return G-np.eye(2*N1)
            
            err = 1
            itercount = 0
            while err > tol and itercount < maxiter:
                    Jac = myJacF(k1,k2)
                    Fval = myF(k1,k2)
                    kappa=-np.linalg.solve(Jac,Fval)
                    k1=kappa[0:N1]+k1
                    k2=kappa[N1:2*N1+1]+k2
                    err=np.max(np.abs(myF(k1,k2)))
                    itercount += 1

            result= y_old+h/2.0*(k1+k2)
            
            return result




