import logging


def setup_logger() -> logging.Logger:
    """
    Sets up the logging configuration for the application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        filename="InvBinderBot.log",
        filemode="a",  # Append mode
        encoding="utf-8",
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up")

    return logger
