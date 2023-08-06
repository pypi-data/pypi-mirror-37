from pick import pick
from subprocess import check_output
import importlib.util
import sys
import os
name = "python_commander"


class Commander:
    commands = [
        {
            "command": 'test_commander',
            "action": 'echo "The commander is ready give out orders"',
            "description": "Test out the commander"
        }
    ]

    @classmethod
    def command(cls, command, action, description=''):
        cls.commands.append(
            {"command": command, "action": action, 'description': description})

    @classmethod
    def take_action(cls, args):
        command = args[1]

        for list_command in cls.commands:
            if list_command['command'] == command:
                if hasattr(list_command['action'], '__call__'):
                    return list_command['action']()
                else:
                    result = check_output(
                        list_command['action'], shell=True).decode('utf-8').rstrip()
                    if result.startswith('"') and result.endswith('"'):
                        result = result[1:len(result) - 1]
                    return result

    @classmethod
    def list_possible_commands(cls):

        list_commands = []
        for command in cls.commands:
            if command['description'] is not '':
                list_commands.append(
                    {'command': command['command'], 'description': command['description'], 'action': command['action']})
            else:
                list_commands.append(
                    {'command': command['command'], 'action': command['action']})

        chosenAction, index = pick(
            list_commands, title="Pick a command:", indicator='->')

        return cls.take_action([None, chosenAction['command']])

    @classmethod
    def give_output(cls, output):
        print(output)

    @classmethod
    def gather_commands(cls):
        root_dir = os.getcwd()
        commands_path = os.path.join(root_dir, 'commands.py')

        spec = importlib.util.spec_from_file_location(
            "set_commands", commands_path)
        commands = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(commands)

    @classmethod
    def execute_commands(cls):
        if __name__ == '__main__':
            if len(sys.argv) > 1:
                Commander.give_output(Commander.take_action(sys.argv))
            else:
                Commander.give_output(Commander.list_possible_commands())
