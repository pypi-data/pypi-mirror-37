import unittest
from commander.commander import Commander


class CommanderTest(unittest.TestCase):
    def setUp(self):
        Commander.commands = []

    def test_giving_command_to_commander(self):
        Commander.command('test', 'echo "Hello"')
        self.assertEqual(len(Commander.commands), 1)

    def test_action_is_added_in_correct_format(self):
        Commander.command('test', 'echo "Hello"')
        self.assertListEqual(Commander.commands, [
            {
                'command': 'test',
                'action': 'echo "Hello"',
                'description': ''
            }
        ])

    def test_passing_function_to_commander_as_action(self):
        def fake_function():
            return "Foo"
        Commander.command('test', fake_function)
        self.assertTrue(hasattr(Commander.commands[0]['action'], '__call__'))
        self.assertEqual(Commander.take_action(['filler', 'test']), 'Foo')

    def test_shell_command_returns_value(self):
        Commander.command('test', 'echo Hello')
        self.assertEqual(Commander.take_action(['filler', 'test']), 'Hello')
