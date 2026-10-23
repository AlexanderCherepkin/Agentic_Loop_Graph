"""Comprehensive Logging Configuration."""
import logging
from datetime import datetime
import json
from typing import Optional


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_no": record.lineno,
        }

        if hasattr(record, "user_id"):
            log_data["user_id"] = getattr(record, "user_id")
        if hasattr(record, "request_id"):
            log_data["request_id"] = getattr(record, "request_id")
        if hasattr(record, "data"):
            log_data["data"] = getattr(record, "data")

        return json.dumps(log_data)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    include_console: bool = True,
):
    """Configure logging for the application."""
    
    # Create logger
    logger = logging.getLogger("figma_export")
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler with JSON formatter
    if include_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger


def create_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Create and configure a named logger."""
    logger = logging.getLogger(f"figma_export.{name}")
    
    # If not configured globally, setup basic config
    if not logger.handlers:
        setup_logging(level=level)

    return logger


# Pre-configured loggers
logger_main = create_logger("main")
logger_api = create_logger("api")
logger_figma = create_logger("figma")
logger_workflow = create_logger("workflow")
logger_security = create_logger("security")