import logging
import logging.config
import os
from pathlib import Path
import sys
from dotenv import load_dotenv

class LoggingConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.configure_logging()
        return cls._instance

    def configure_logging(self):
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
            # Create directory structure if needed
            log_path = Path(log_output)
            try:
                log_path.parent.mkdir(parents=True, exist_ok=True)
                config['handlers']['file']['filename'] = str(log_path)
                config['handlers']['file']['level'] = log_level
                config['loggers']['app']['handlers'] = ['file']
            except PermissionError as pe:
                sys.stderr.write(f"Permission denied creating log file: {pe}\n")
                sys.exit(1)
            except Exception as e:
                sys.stderr.write(f"Error configuring file logging: {e}\n")
                sys.exit(1)

        logging.config.dictConfig(config)
