from subprocess import check_output

from pick import pick


class Commander:
    commands = []

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
    def giveOutput(cls, output):
        print(output)
