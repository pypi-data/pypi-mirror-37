"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""

from prompt_toolkit.key_binding import KeyBindings


key_bindings = KeyBindings()


@key_bindings.add(u'c-c')
@key_bindings.add(u'c-q')
def _(event):
    " Pressing Ctrl-Q or Ctrl-C will exit the user interface. "
    event.app.exit()
