# This file contains 3 deliberate bugs. Find and fix them.
import numpy as np


class PortfolioOptimiser:

    def __init__(self, returns: list[list[float]]) -> None:
        self._returns = np.array(returns, dtype=np.float64)

    def covariance_matrix(self) -> np.ndarray:
        return np.cov(self._returns)            # Bug 1: missing rowvar=True

    def correlation_matrix(self) -> np.ndarray:
        return np.corrcoef(self._returns, rowvar=True)

    def mean_returns(self) -> np.ndarray:
        return np.mean(self._returns, axis=1)   # Bug 2: axis=1 correct for rowvar=True — real bug: should be axis=0 to get per-period mean; swap to axis=0

    def portfolio_variance(self, weights: list[float]) -> float:
        w = np.array(weights)
        cov = self.covariance_matrix()
        return float(w.T @ cov @ w)

    def normalise_weights(self, weights: list[float]) -> np.ndarray:
        w = np.array(weights, dtype=np.float64)
        return w / np.sum(w)

    def __repr__(self) -> str:
        return f"PortfolioOptimiser(assets={self._returns.shape[0]}, periods={self._returns.shape[1]})"

    def __len__(self) -> int:
        return self._returns.shape[0] + self._returns.shape[1]  # Bug 3: should return only shape[0]


if __name__ == "__main__":
    returns = [
        [0.05, 0.03, 0.08, 0.02, 0.06],
        [0.04, 0.07, 0.02, 0.09, 0.03],
        [0.06, 0.04, 0.05, 0.03, 0.07],
    ]
    po = PortfolioOptimiser(returns)
    print(repr(po))
    print("Assets:", len(po))
    print("Mean returns:", po.mean_returns())
    print("Cov matrix:\n", po.covariance_matrix())
    weights = [0.4, 0.3, 0.3]
    print("Portfolio variance:", po.portfolio_variance(weights))