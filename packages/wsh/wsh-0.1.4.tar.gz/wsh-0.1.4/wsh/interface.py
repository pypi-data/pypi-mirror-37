# flake8: noqa
"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import click
from platform import python_version
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea, SearchToolbar
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import JsonLexer
from .command_processor import CommandProcessor, Command


# Utilities
# ---------
def init_text():
    """Returns the introductory text applied to output when the app is launched."""
    return (u'[wsh "{}"] (Python "{}")\n'.format(__version__, python_version()) +
            u'\nType "help" for more info, or "exit" to quit.\n' +
            u'-' * click.get_terminal_size()[0])


# Command Processor
command_processor = CommandProcessor()

# Output Field
# ------------
output_field = TextArea(text=init_text(),
                        lexer=PygmentsLexer(JsonLexer))


# Input Field
# -----------
def accept_handler(buf):
    """Callback method invoked when <ENTER> is pressed."""
    command_processor.accept_handler(buf, input_field, output_field)


command_completer = WordCompleter([command.value for command in Command],
                                  ignore_case=True)

input_field = TextArea(height=1,
                       prompt=u'>>> ',
                       lexer=PygmentsLexer(JsonLexer),
                       completer=command_completer,
                       style='class:input-field',
                       multiline=False,
                       wrap_lines=False,
                       accept_handler=accept_handler)

# Container
# ---------
container = HSplit([output_field,
                    Window(height=1, char=u'-', style=u'class:line'),
                    input_field])
