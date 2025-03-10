# Advanced Python Calculator Mid Term

## Project Overview

This midterm assignment involves creating a  Python-based calculator application. The project emphasizes software engineering best practices, including writing maintainable code, implementing appropriate design patterns, incorporating comprehensive logging systems, utilizing environment variables for dynamic configuration, leveraging Pandas for data operations, and developing an interactive command-line interface (REPL) for user interaction.

## Prerequisites

- Python
- pip

  
## Installation

1. Clone the repository:

```
git clone https://github.com/srikargoud2002/Mid_Term
```

2. Navigate to the project directory:

```
cd Mid_Term
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To start the calculator, run the following command

```
python main.py
```

This will launch the REPL interface, where you can perform arithmetic operations, manage calculation history, and access additional functionalities through plugins.

## Commands
- `menu`: Lists all available plugins.
- `add <operand1> <operand2>`: Performs addition of two numbers.
- `subtract <operand1> <operand2>`: Performs subtraction of two numbers.
- `multiply <operand1> <operand2>`: Performs multiplication of two numbers.
- `divide <operand1> <operand2>`: Performs division of two numbers.
- `history_show`: Displays the calculation history.
- `history_clear`: Clears the calculation history.
- `history_save` : Saves the history into a csv file with date and time.
- `history_load` : It is for loading the history from the available csv files.
- `last_op`: Shows the last operation performed
- `exit`: Exits the calculator application.

## Plugins

The calculator supports dynamic loading of plugins. Even the menu is fetched by loading all the plugins. If there is any new plugin added it will automatically load into the menu.

## Features

- **Command-Line Interface (REPL)**: An interactive environment for performing arithmetic operations and managing calculation history.
- **Plugin System**: A system to extend functionalities through dynamically loaded plugins.
- **Calculation History Management with Pandas**: Leverages Pandas for robust management of calculation history.
- **Comprehensive Logging**: Implements detailed logging for operations, errors, and informational messages.
- **Design Patterns**: 
    - **Facade Pattern** : It is implemented in the history management.
    - **Command Pattern** : It is implemented in the commands management.
    - **Factory Method** : It is implemented in the calculation.py .
    
  
The design patterns used in this project promote modularity, extensibility, and maintainability. For more details on their implementation and impact, please refer to the respective sections in the source code.


## Logging

The calculator application uses a comprehensive logging system to record detailed application operations, data manipulations, errors, and informational messages. The logging system supports different log levels (INFO, WARNING, ERROR) setting via environment variables.

## Environment Variables

Environment variables are used to set logging levels dynamically, output path of the logs, history saving path and the Environment.

LOG_LEVEL=DEBUG  # INFO, WARNING, ERROR, CRITICAL
LOG_OUTPUT=./logs/app.log
HISTORY_PATH=./calculator_history
ENVIRONMENT= DEVELOPMENT

## Testing & Coverage

Run the following command to execute tests and ensure the application behaves as expected:

```bash
pytest
```
Run this to get coverage

```bash
pytest --pylint --cov
```
## EAFP & LBYL

**LBYL(Look Before You Leap)**
This approach is used to validate conditions before attempting operations.

Code example

```
        if command_name in self.command_handler.commands:
            command = self.command_handler.commands[command_name]
            if callable(command.execute):
                command.execute(*args) if args else command.execute()
            else:
                print("Command is not executable")
        else:
            print(f"No such command: {command_name}")
```
**Easier to Ask for Forgiveness than Permission)**

This approach attempts execution directly and handles any resulting exceptions.

Code Example:

```
    def _process_plugin_module(self, plugins_package: str, plugin_name: str):
        try:
            plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
            self._register_commands_from_module(plugin_module, plugin_name)
        except Exception as error: 
            self.logger.error("Error loading plugin %s: %s", plugin_name, str(error), exc_info=True)
```



