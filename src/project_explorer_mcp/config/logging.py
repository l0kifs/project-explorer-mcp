import sys

from loguru import logger

from .settings import get_settings

settings = get_settings()


def setup_logging():
    """
    Configure logging for the application.
    """

    # Remove default handler to avoid duplicate logs
    logger.remove()

    # Console handler - for development/debugging
    logger.add(
        sys.stderr,
        level=settings.logging_level,
        format=settings.logging_console_format,
        colorize=True,  # Enable colors in console
        backtrace=True,  # Show full traceback on errors
        diagnose=True,  # Show variable values in tracebacks (disable in production for security)
        enqueue=True,  # Thread-safe logging
        catch=True,  # Catch and log logging errors
    )

    # File handler - structured JSON logging
    logger.add(
        settings.logging_file_dir + "/app.log",
        level=settings.logging_file_level,
        serialize=True,  # JSON serialization
        rotation="10 MB",  # Rotate when file reaches 10MB
        retention="30 days",  # Keep logs for 30 days
        compression="gz",  # Compress rotated files
        encoding="utf-8",
        enqueue=True,
        catch=True,
    )

    # Configure common context (can be overridden per module)
    logger.configure(extra={"app": settings.app_name, "version": settings.app_version})

    # Log startup message
    logger.info(
        "Logging system initialized",
        log_file=str(settings.logging_file_dir + "/app.log"),
        log_level=settings.logging_level,
    )
