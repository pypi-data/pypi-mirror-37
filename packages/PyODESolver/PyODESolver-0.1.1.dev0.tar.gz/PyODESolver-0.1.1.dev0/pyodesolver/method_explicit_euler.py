from step_method import StepMethod


class ExplicitEuler(StepMethod):

    """
        This class implements the explicit_euler method for solving
        ordinary differential equations.
    """

    def step(self, func, uvec, time, steplen):
        return uvec + steplen * func.eval(uvec, time)
