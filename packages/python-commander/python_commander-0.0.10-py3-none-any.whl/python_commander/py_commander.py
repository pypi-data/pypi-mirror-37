from . import Commander

def commander_start():
    Commander.gather_commands()
    Commander.execute_commands()
