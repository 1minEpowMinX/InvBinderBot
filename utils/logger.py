from logging import basicConfig, getLogger, INFO, Logger, StreamHandler, FileHandler
from pathlib import Path
from sys import stdout


def setup_logger(path: Path) -> Logger:
    """
    Sets up the logging configuration for the application.

    This function configures the logging system to log messages to a file and the console.
    Console logging is particularly useful for environments like Kubernetes.

    Args:
        path (Path): The path where the log file will be stored.

    Returns:
        Logger: Configured logger instance.
    """

    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    fileHandler = FileHandler(path, mode="a", encoding="utf-8")
    streamHandler = StreamHandler(stdout)  # Log to console for kubernetes

    basicConfig(  # Can implement RotatingFileHandler in the future if needed
        level=INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
        handlers=[fileHandler, streamHandler],
    )

    logger = getLogger(__name__)
    logger.info("Logging is set up")

    return logger
