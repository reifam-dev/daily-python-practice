"""Day 170 - Anomaly Detection (EMA): Error Quiz. Find and fix three bugs."""
class EmaAnomalyDetector:
    def __init__(self, alpha: float, threshold_pct: float):
        self.alpha = alpha
        self.threshold_pct = threshold_pct
        self.ema = None

    def check(self, value: float) -> bool:
        if self.ema is None:
            self.ema = value
            return False

        deviation = abs(value - self.ema) / self.ema
        is_anomaly = deviation > self.threshold_pct

        self.ema = self.alpha * value + self.ema

        return is_anomaly


if __name__ == "__main__":
    detector = EmaAnomalyDetector(alpha=0.3, threshold_pct=0.5)
    values = [100, 102, 98, 101, 500, 99, 103]
    for v in values:
        print(f"{v}: anomaly={detector.check(v)}")