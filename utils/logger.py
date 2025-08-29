from logging import basicConfig, getLogger, INFO, Logger


def setup_logger() -> Logger:
    """
    Sets up the logging configuration for the application.

    Returns:
        Logger: Configured logger instance.
    """

    basicConfig(
        filename="InvBinderBot.log",
        filemode="a",  # Append mode
        encoding="utf-8",
        level=INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    logger = getLogger(__name__)
    logger.info("Logging is set up")

    return logger
