from __future__ import absolute_import

from pipenv.patched.notpip._internal.basecommand import SUCCESS, Command
from pipenv.patched.notpip._internal.exceptions import CommandError


class HelpCommand(Command):
    """Show help for commands"""
    name = 'help'
    usage = """
      %prog <command>"""
    summary = 'Show help for commands.'
    ignore_require_venv = True

    def run(self, options, args):
        from pipenv.patched.notpip._internal.commands import commands_dict, get_similar_commands

        try:
            # 'pip help' with no args is handled by pip.__init__.parseopt()
            cmd_name = args[0]  # the command we need help for
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            guess = get_similar_commands(cmd_name)

            msg = ['unknown command "%s"' % cmd_name]
            if guess:
                msg.append('maybe you meant "%s"' % guess)

            raise CommandError(' - '.join(msg))

        command = commands_dict[cmd_name]()
        command.parser.print_help()

        return SUCCESS
