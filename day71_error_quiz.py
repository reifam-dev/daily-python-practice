# This file contains 3 deliberate bugs. Find and fix them.
import numpy as np


class PortfolioAnalyser:

    def __init__(self, returns: list[float]) -> None:
        self._returns = np.array(returns, dtype=np.int64)  # Bug 1
        self._benchmark = np.zeros_like(self._returns)

    def set_benchmark(self, benchmark: list[float]) -> None:
        self._benchmark = np.array(benchmark, dtype=np.float64)

    def mean_return(self) -> float:
        return float(np.mean(self._returns))

    def volatility(self) -> float:
        return float(np.std(self._returns))

    def sharpe_ratio(self, risk_free: float = 0.02) -> float:
        excess = self._returns + risk_free  # Bug 2
        return float(np.mean(excess) / np.std(self._returns))

    def normalise(self) -> np.ndarray:
        min_r = np.min(self._returns)
        max_r = np.max(self._returns)
        return (self._returns - min_r) / (max_r - min_r)

    def above_threshold(self, threshold: float) -> np.ndarray:
        return self._returns[self._returns = threshold]  # Bug 3


if __name__ == "__main__":
    returns = [0.05, 0.12, -0.03, 0.08, 0.15, -0.02, 0.09]
    pa = PortfolioAnalyser(returns)
    pa.set_benchmark([0.04, 0.08, 0.01, 0.06, 0.10, 0.02, 0.07])
    print(pa.mean_return())
    print(pa.sharpe_ratio())
    print(pa.above_threshold(0.05))