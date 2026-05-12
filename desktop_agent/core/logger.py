"""
Logging system for the desktop agent.
Provides timestamped, colored logging with file output support.
"""

import logging
import sys
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Formatter with colored output for terminal."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    SECTIONS = {
        'OBSERVE': '\033[34m',    # Blue
        'PLAN': '\033[35m',       # Magenta
        'ACTION': '\033[33m',     # Yellow
        'VERIFY': '\033[36m',     # Cyan
        'EXECUTE': '\033[32m',    # Green
    }
    
    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, '')
        reset = self.COLORS['RESET']
        
        # Check for section markers in message
        for section, section_color in self.SECTIONS.items():
            if record.msg.startswith(section):
                color = section_color
                break
        
        record.levelname = f"{color}{levelname}{reset}"
        record.msg = f"{color}{record.msg}{reset}"
        
        return super().format(record)


def setup_logger(name='desktop_agent', log_file=None):
    """
    Setup logger with console and optional file output.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    formatter = ColoredFormatter(
        fmt='[%(asctime)s] %(levelname)-8s %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


# Logging helpers for key sections
def log_section(section_name, details=""):
    """Log a major section marker."""
    msg = section_name
    if details:
        msg += f": {details}"
    logger.info(msg)


def log_action(action_name, params=""):
    """Log an action execution."""
    msg = f"ACTION: {action_name}"
    if params:
        msg += f"({params})"
    logger.info(msg)


def log_result(success, details=""):
    """Log an action result."""
    status = "✓ SUCCESS" if success else "✗ FAILED"
    msg = f"{status}"
    if details:
        msg += f": {details}"
    logger.info(msg)


def log_memory_event(event_type, node_id="", details=""):
    """Log memory graph events."""
    msg = f"MEMORY [{event_type}]: {node_id}"
    if details:
        msg += f" - {details}"
    logger.debug(msg)
