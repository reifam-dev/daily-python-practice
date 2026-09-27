"""Day 170 - Anomaly Detection (EMA): flags a value as anomalous when
it deviates too far from a smoothly-tracked exponential moving
average, without letting the anomaly itself corrupt the running
average it's compared against - PCPP1 standard."""
from __future__ import annotations


class EmaAnomalyDetector:
    def __init__(self, alpha: float, threshold_pct: float) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0.0, 1.0]")
        self.alpha = alpha
        self.threshold_pct = threshold_pct
        self.ema: float | None = None

    def check(self, value: float) -> bool:
        """Return True if value is an anomaly; update the EMA either way."""
        if self.ema is None:
            self.ema = value
            return False

        deviation = abs(value - self.ema) / self.ema
        is_anomaly = deviation > self.threshold_pct

        self.ema = self.alpha * value + (1 - self.alpha) * self.ema

        return is_anomaly


if __name__ == "__main__":
    detector = EmaAnomalyDetector(alpha=0.3, threshold_pct=0.5)
    values = [100, 102, 98, 101, 500, 99, 103]
    for v in values:
        print(f"{v}: anomaly={detector.check(v)}")