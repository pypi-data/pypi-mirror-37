import numpy as np


class StepMethod(object):

    """Docstring for step_method.
        Time stepping method for ODE's
    """

    def __init__(self, N, y0, domain, func):
        """TODO: to be defined1. """
        self.N = N
        self.y0 = y0
        self.domain = domain
        self.func = func

    def setGrid(self, domain, N):
        self.domain = domain
        self.N = N

    def setFunc(self, func):
        self.func = func

    def generate(self):
        t_start, t_end = self.domain
        t_grid = np.linspace(t_start, t_end, self.N)
        steplen = t_grid[1] - t_grid[0]
        (time, uvec) = (t_start, self.y0)
        yield (time, uvec)
        for t_idx in range(len(t_grid)-1):
            time = t_grid[t_idx]
            uvec = self.step(self.func, uvec, time, steplen)
            yield (time, uvec)

    def step(self, f, u, t, h):
        raise NotImplementedError
