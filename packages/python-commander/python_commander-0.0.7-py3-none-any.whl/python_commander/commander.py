import sys
from commander.commander import Commander

Commander.command('test', 'echo "Commander is ready for action!"',
                  description="Write 444 to the console")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        Commander.giveOutput(Commander.take_action(sys.argv))
    else:
        Commander.giveOutput(Commander.list_possible_commands())
