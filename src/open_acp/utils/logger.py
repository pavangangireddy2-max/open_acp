"""Structured logging setup using structlog."""
import structlog

from open_acp.config.settings import get_settings


def setup_logging() -> None:
    """Configure structlog for the application."""
    settings = get_settings()
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog, settings.log_level.upper(), structlog.INFO) if hasattr(structlog, settings.log_level.upper()) else 20
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "open_acp"):
    """Get a bound logger."""
    return structlog.get_logger(name)
