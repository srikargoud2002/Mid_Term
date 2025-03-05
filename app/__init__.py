import os
from app.commands import CommandHandler
from dotenv import load_dotenv
import importlib
from app.commands import Command
import pkgutil


class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.load_environment()


    def load_environment(self):
        load_dotenv()
        self.settings = dict(os.environ)
        environment = self.get_environment_variable()
        print(f"Environment loaded: {environment}")

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            return

        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')

                    for item_name in dir(plugin_module):
                        item = getattr(plugin_module, item_name)
                        try:
                            if issubclass(item, Command) and item != Command:
                                if item_name == 'MenuCommand':
                                    self.command_handler.register_command(plugin_name, item(self.command_handler))
                                else:
                                    self.command_handler.register_command(plugin_name, item())
                        except TypeError:
                            continue
                except Exception as e:
                    print(f"Error loading plugin {plugin_name}: {str(e)}")                    


    def run_repl(self):
        """Runs the Read-Eval-Print Loop (REPL) for the application."""
        print("Welcome to Calculator (Press Ctrl+C to exit)")

        try:
            while True:
                user_input = input(">>> ").strip()

                if user_input.lower() == 'exit':
                    self.command_handler.execute_command('exit')
                    break

                parts = user_input.split()
                command_name = parts[0]
                args = parts[1:]

                if command_name in self.command_handler.commands:
                    command = self.command_handler.commands[command_name]

                    try:
                        if args:
                            command.execute(*args)
                        else:
                            command.execute()
                    except Exception as e:
                        print(f"Error: {str(e)}")
                else:
                    print(f"No such command: {command_name}")
        
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting gracefully...")



    def start(self):
        """Starts the application and enters REPL mode."""
        self.load_plugins()
        self.run_repl()
