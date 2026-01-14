class Fscore:
    def __init__(self, f_type="Greedy") -> None:
        self.f_type = f_type

        self._f = {
            "Default": self._astar,
            "UniformCost": self._uniform,
            "Greedy": self._greedy,
            # "Wacky": self._wacky,
        }[f_type]

    def f(self, g: float, h: float) -> float:
        return self._f(g, h)

    @staticmethod
    def _astar(g, h):
        return g + h

    @staticmethod
    def _uniform(g, h):
        return g

    @staticmethod
    def _greedy(g, h):
        return h

    # @staticmethod
    # def _wacky(g, h):
    #     return h + h * 10
