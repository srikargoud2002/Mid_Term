import os
from app.commands import CommandHandler
from dotenv import load_dotenv
import importlib
from app.commands import Command
import pkgutil
from logging_custom.logging_config import LoggingConfig
import logging

class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.command_handler = CommandHandler()
        self.load_environment()
        LoggingConfig()
        self.logger.info("Application initialized")

    def load_environment(self):
        try:
            load_dotenv()
            self.settings = dict(os.environ)
            environment = self.get_environment_variable()
            self.logger.info("Environment variables loaded successfully")
            self.logger.debug(f"Current environment: {environment}")
        except Exception as e:
            self.logger.critical("Failed to load environment variables", exc_info=True)
            raise

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        value = self.settings.get(env_var, None)
        if not value:
            self.logger.warning(f"Environment variable {env_var} not set")
        return value

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        
        self.logger.info("Starting plugin loading process")
        
        if not os.path.exists(plugins_path):
            self.logger.error(f"Plugin directory {plugins_path} not found")
            return

        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.logger.debug(f"Discovered plugin: {plugin_name}")

                    for item_name in dir(plugin_module):
                        item = getattr(plugin_module, item_name)
                        try:
                            if issubclass(item, Command) and item != Command:
                                if item_name == 'MenuCommand':
                                    self.command_handler.register_command(plugin_name, item(self.command_handler))
                                else:
                                    self.command_handler.register_command(plugin_name, item())
                                self.logger.info(f"Registered command: {plugin_name}")
                        except TypeError:
                            continue
                except Exception as e:
                    self.logger.error(f"Error loading plugin {plugin_name}: {str(e)}", exc_info=True)
                    continue

    def run_repl(self):
        self.logger.info("Starting REPL interface")
        print("Welcome to Calculator (Press Ctrl+C to exit)")

        try:
            while True:
                try:
                    user_input = input(">>> ").strip()
                    self.logger.debug(f"User input: {user_input}")

                    if user_input.lower() == 'exit':
                        self.command_handler.execute_command('exit')
                        self.logger.info("Exit command received")
                        break

                    parts = user_input.split()
                    command_name = parts[0]
                    args = parts[1:]

                    if command_name in self.command_handler.commands:
                        command = self.command_handler.commands[command_name]
                        self.logger.info(f"Executing command: {command_name} with args: {args}")

                        try:
                            if args:
                                command.execute(*args)
                            else:
                                command.execute()
                        except Exception as e:
                            self.logger.error(f"Command execution error: {str(e)}", exc_info=True)
                            print(f"Error: {str(e)}")
                    else:
                        self.logger.warning(f"Unknown command attempted: {command_name}")
                        print(f"No such command: {command_name}")
                        
                except KeyboardInterrupt:
                    self.logger.info("Keyboard interrupt detected")
                    print("\nExiting...")
                    break

        except Exception as e:
            self.logger.critical("REPL session failed", exc_info=True)
            raise

    def start(self):
        self.logger.info("Application starting")
        try:
            self.load_plugins()
            self.run_repl()
        except Exception as e:
            self.logger.critical("Application failed to start", exc_info=True)
            raise
        finally:
            self.logger.info("Application shutdown")