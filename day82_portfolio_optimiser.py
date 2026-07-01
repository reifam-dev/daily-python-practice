"""
Day 82 – NumPy Advanced: linear algebra, covariance, correlation, eigen decomposition.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import numpy as np
from numpy.typing import NDArray


class PortfolioOptimiser:
    """
    Multi-asset portfolio optimisation using NumPy linear algebra.
    Each row in the returns matrix represents one asset's return series.
    """

    def __init__(self, returns: list[list[float]]) -> None:
        """Initialise with a 2D list of asset returns.

        Args:
            returns: List of lists where each inner list is one asset's
                     periodic return series (e.g. monthly returns).
        """
        self._returns: NDArray[np.float64] = np.array(returns, dtype=np.float64)

    def covariance_matrix(self) -> NDArray[np.float64]:
        """Compute the covariance matrix across assets.

        Returns:
            Square covariance matrix of shape (n_assets, n_assets).
        """
        return np.cov(self._returns, rowvar=True)

    def correlation_matrix(self) -> NDArray[np.float64]:
        """Compute the correlation matrix across assets.

        Returns:
            Square correlation matrix of shape (n_assets, n_assets).
        """
        return np.corrcoef(self._returns, rowvar=True)

    def mean_returns(self) -> NDArray[np.float64]:
        """Compute mean return per asset across all periods.

        Returns:
            1D array of mean returns, one per asset.
        """
        return np.mean(self._returns, axis=1)

    def portfolio_variance(self, weights: list[float]) -> float:
        """Compute portfolio variance given asset weights.

        Args:
            weights: List of asset weights; must sum to 1.

        Returns:
            Portfolio variance as a float.
        """
        w: NDArray[np.float64] = np.array(weights, dtype=np.float64)
        cov = self.covariance_matrix()
        return float(w.T @ cov @ w)

    def portfolio_volatility(self, weights: list[float]) -> float:
        """Compute portfolio volatility (standard deviation) given weights.

        Args:
            weights: List of asset weights; must sum to 1.

        Returns:
            Portfolio volatility as a float.
        """
        return float(np.sqrt(self.portfolio_variance(weights)))

    def normalise_weights(self, weights: list[float]) -> NDArray[np.float64]:
        """Normalise weights so they sum to 1.

        Args:
            weights: Raw weight values.

        Returns:
            Normalised weight array.
        """
        w: NDArray[np.float64] = np.array(weights, dtype=np.float64)
        return w / np.sum(w)

    def eigen_decomposition(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Perform eigen decomposition of the covariance matrix.

        Returns:
            Tuple of (eigenvalues, eigenvectors).
        """
        cov = self.covariance_matrix()
        values, vectors = np.linalg.eig(cov)
        return values, vectors

    def sharpe_ratios(self, risk_free: float = 0.02) -> NDArray[np.float64]:
        """Compute per-asset Sharpe ratios.

        Args:
            risk_free: Annual risk-free rate; defaults to 0.02.

        Returns:
            1D array of Sharpe ratios, one per asset.
        """
        means = self.mean_returns()
        stds = np.std(self._returns, axis=1)
        return (means - risk_free) / stds

    def __len__(self) -> int:
        """Return the number of assets in the portfolio.

        Returns:
            Integer count of assets.
        """
        return int(self._returns.shape[0])

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this optimiser.
        """
        return (
            f"PortfolioOptimiser(assets={self._returns.shape[0]}, "
            f"periods={self._returns.shape[1]})"
        )


if __name__ == "__main__":
    returns: list[list[float]] = [
        [0.05, 0.03, 0.08, 0.02, 0.06],
        [0.04, 0.07, 0.02, 0.09, 0.03],
        [0.06, 0.04, 0.05, 0.03, 0.07],
    ]

    po = PortfolioOptimiser(returns)
    print(repr(po))
    print(f"Assets: {len(po)}")
    print(f"Mean returns:       {po.mean_returns()}")
    print(f"Covariance matrix:\n{po.covariance_matrix()}")
    print(f"Correlation matrix:\n{po.correlation_matrix()}")

    weights = [0.4, 0.3, 0.3]
    norm_w = po.normalise_weights(weights)
    print(f"Normalised weights:  {norm_w}")
    print(f"Portfolio variance:  {po.portfolio_variance(norm_w.tolist()):.6f}")
    print(f"Portfolio volatility:{po.portfolio_volatility(norm_w.tolist()):.6f}")
    print(f"Sharpe ratios:       {po.sharpe_ratios()}")

    eigenvalues, eigenvectors = po.eigen_decomposition()
    print(f"Eigenvalues:         {eigenvalues}")