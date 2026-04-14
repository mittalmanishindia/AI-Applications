"""
Logging configuration for AI Text Summarization Agent
Provides structured logging with file rotation and multiple log levels
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
ERROR_LOG = LOGS_DIR / "error.log"
INFO_LOG = LOGS_DIR / "info.log"
DEBUG_LOG = LOGS_DIR / "debug.log"
ACCESS_LOG = LOGS_DIR / "access.log"


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Build colored log message
        log_message = (
            f"{color}[{record.levelname}]{reset} "
            f"{timestamp} - "
            f"{record.name} - "
            f"{record.getMessage()}"
        )
        
        # Add exception info if present
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"
        
        return log_message


def setup_logger(name: str = "summarization_agent") -> logging.Logger:
    """
    Set up and configure logger with multiple handlers
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    # Error log handler (rotating file)
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    logger.addHandler(error_handler)
    
    # Info log handler (rotating file)
    info_handler = logging.handlers.RotatingFileHandler(
        INFO_LOG,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(JSONFormatter())
    logger.addHandler(info_handler)
    
    # Debug log handler (rotating file)
    debug_handler = logging.handlers.RotatingFileHandler(
        DEBUG_LOG,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,
        encoding='utf-8'
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(JSONFormatter())
    logger.addHandler(debug_handler)
    
    return logger


def get_access_logger() -> logging.Logger:
    """
    Get logger for API access logs
    
    Returns:
        Access logger instance
    """
    logger = logging.getLogger("access")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    # Access log handler
    access_handler = logging.handlers.RotatingFileHandler(
        ACCESS_LOG,
        maxBytes=20 * 1024 * 1024,  # 20 MB
        backupCount=10,
        encoding='utf-8'
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(JSONFormatter())
    logger.addHandler(access_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()
access_logger = get_access_logger()
