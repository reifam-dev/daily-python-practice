"""
Day 71 – Advanced NumPy: Array Operations, Broadcasting & Vectorisation
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import numpy as np
from numpy.typing import NDArray


class PortfolioAnalyser:
    """Analyses portfolio returns using NumPy vectorised operations."""

    def __init__(self, returns: list[float]) -> None:
        """Initialise the analyser with a list of periodic returns.

        Args:
            returns: A list of float return values (e.g. 0.05 for 5%).
        """
        self._returns: NDArray[np.float64] = np.array(returns, dtype=np.float64)
        self._benchmark: NDArray[np.float64] = np.zeros_like(self._returns)

    def set_benchmark(self, benchmark: list[float]) -> None:
        """Set a benchmark return series for comparison.

        Args:
            benchmark: A list of float benchmark returns, same length as returns.
        """
        self._benchmark = np.array(benchmark, dtype=np.float64)

    def mean_return(self) -> float:
        """Calculate the arithmetic mean return.

        Returns:
            Mean of the return series as a float.
        """
        return float(np.mean(self._returns))

    def volatility(self) -> float:
        """Calculate the standard deviation (volatility) of returns.

        Returns:
            Standard deviation as a float.
        """
        return float(np.std(self._returns))

    def sharpe_ratio(self, risk_free: float = 0.02) -> float:
        """Calculate the Sharpe ratio using vectorised broadcasting.

        Args:
            risk_free: Annual risk-free rate; defaults to 0.02 (2%).

        Returns:
            Sharpe ratio as a float.
        """
        excess: NDArray[np.float64] = self._returns - risk_free
        return float(np.mean(excess) / np.std(self._returns))

    def active_returns(self) -> NDArray[np.float64]:
        """Calculate active returns relative to the benchmark via broadcasting.

        Returns:
            NumPy array of active (excess vs benchmark) returns.
        """
        return self._returns - self._benchmark

    def normalise(self) -> NDArray[np.float64]:
        """Normalise returns to the [0, 1] range using min-max scaling.

        Returns:
            NumPy array of normalised return values.
        """
        min_r: np.float64 = np.min(self._returns)
        max_r: np.float64 = np.max(self._returns)
        return (self._returns - min_r) / (max_r - min_r)

    def above_threshold(self, threshold: float) -> NDArray[np.float64]:
        """Filter returns above a given threshold using boolean indexing.

        Args:
            threshold: The minimum return value to include.

        Returns:
            NumPy array of returns that exceed the threshold.
        """
        return self._returns[self._returns > threshold]

    def cumulative_return(self) -> float:
        """Calculate the cumulative compounded return across all periods.

        Returns:
            Cumulative return as a float.
        """
        return float(np.prod(1 + self._returns) - 1)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for the PortfolioAnalyser instance.
        """
        return (
            f"PortfolioAnalyser(n={len(self._returns)}, "
            f"mean={self.mean_return():.4f}, "
            f"vol={self.volatility():.4f})"
        )


if __name__ == "__main__":
    returns: list[float] = [0.05, 0.12, -0.03, 0.08, 0.15, -0.02, 0.09]
    benchmark: list[float] = [0.04, 0.08, 0.01, 0.06, 0.10, 0.02, 0.07]

    pa = PortfolioAnalyser(returns)
    pa.set_benchmark(benchmark)

    print(f"Mean return   : {pa.mean_return():.4f}")
    print(f"Volatility    : {pa.volatility():.4f}")
    print(f"Sharpe ratio  : {pa.sharpe_ratio():.4f}")
    print(f"Active returns: {pa.active_returns()}")
    print(f"Normalised    : {pa.normalise()}")
    print(f"Above 5%      : {pa.above_threshold(0.05)}")
    print(f"Cumulative    : {pa.cumulative_return():.4f}")
    print(repr(pa))