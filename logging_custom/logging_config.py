"""
Logging configuration module.

This module provides a singleton-based logging configuration setup using 
environment variables for customization.
"""
import logging
import logging.config
import os
from pathlib import Path
import sys
from dotenv import load_dotenv

class LoggingConfig:
    """
    Singleton class for configuring application-wide logging settings.
    """
    _instance = None

    def __new__(cls):
        """Ensures only one instance of LoggingConfig exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.configure_logging()
        return cls._instance

    def configure_logging(self):
        """Configures the logging settings based on environment variables."""
        load_dotenv()
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_output = os.getenv('LOG_OUTPUT', 'console')

        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'stream': sys.stdout
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'maxBytes': 1048576,
                    'backupCount': 3,
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                'app': {
                    'handlers': [],
                    'level': log_level,
                    'propagate': False
                }
            }
        }

        if log_output.lower() == 'console':
            config['loggers']['app']['handlers'] = ['console']
            config['handlers']['console']['level'] = log_level
        else:
            # Ensure log directory exists before setting up file logging
            log_path = Path(log_output)
            try:
                log_path.parent.mkdir(parents=True, exist_ok=True)
                config["handlers"]["file"]["filename"] = str(log_path)
                config["handlers"]["file"]["level"] = log_level
                config["loggers"]["app"]["handlers"] = ["file"]
            except PermissionError:
                sys.stderr.write("Error: Permission denied while creating the log file.\n")
                sys.exit(1)
            except OSError as error:
                sys.stderr.write(f"Error configuring file logging: {error}\n")
                sys.exit(1)

        logging.config.dictConfig(config)
