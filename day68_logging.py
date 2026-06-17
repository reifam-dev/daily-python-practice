# Day 68 - Clean logging module examples
# New concepts: logging levels, handlers, formatters, named loggers, file logging
# PEP 8, docstrings, type hints, exceptions throughout

import logging
import sys
from pathlib import Path
import tempfile


def create_logger(
    name: str,
    level: int = logging.DEBUG,
    log_file: Path = None
) -> logging.Logger:
    """Create and configure a named logger with console and optional file handler.

    Checks for existing handlers to prevent duplicate log entries
    when the function is called multiple times with the same name.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class DataProcessor:
    """Demonstrates logging in a class context."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._logger = create_logger(f"DataProcessor.{name}")

    def process(self, value: float) -> float:
        """Process a value with appropriate logging at each step."""
        self._logger.debug(f"Processing value: {value}")

        if value < 0:
            self._logger.warning(f"Negative value received: {value}. Using absolute.")
            value = abs(value)

        if value > 1000:
            self._logger.error(f"Value {value} exceeds maximum threshold of 1000.")
            raise ValueError(f"Value {value} too large.")

        result = value * 2
        self._logger.info(f"Processed {value} → {result}")
        return result


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "app.log"
        logger = create_logger("main", log_file=log_path)

        print("=== Logging levels ===\n")
        logger.debug("Debug — most detailed, development only")
        logger.info("Info — general operational messages")
        logger.warning("Warning — unexpected but handled")
        logger.error("Error — serious problem")
        logger.critical("Critical — programme may not continue")

        print("\n=== DataProcessor with logging ===\n")
        processor = DataProcessor("Finance")
        try:
            processor.process(42.5)
            processor.process(-10.0)
            processor.process(2000.0)
        except ValueError as e:
            logger.exception(f"Processing failed: {e}")

        print(f"\n=== Log file contents (WARNING+ only) ===\n")
        log_content = log_path.read_text(encoding="utf-8")
        for line in log_content.splitlines():
            print(f"  {line}")