from step_method import StepMethod
import scipy.sparse as sparse

class RK4(StepMethod):

    """
        This implements RK4
    """

    def step(self,func,uvec,time,steplen):
        k1=func.eval(uvec,time)
        k2=func.eval(uvec+steplen*k1/2,time+steplen/2)
        k3=func.eval(uvec+steplen*k2/2,time+steplen/2)
        k4=func.eval(uvec+steplen*k3,time+steplen)
        return uvec+1.0/6.0*steplen*(k1+2.0*k2+2.0*k3+k4)
