"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""

from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from .style import SolarizedStyle
from .interface import input_field, container, command_processor
from .key_bindings import key_bindings


style = style_from_pygments_cls(SolarizedStyle)

app = Application(layout=Layout(container,
                  focused_element=input_field),
                  key_bindings=key_bindings,
                  style=style,
                  include_default_pygments_style=False,
                  color_depth=ColorDepth.DEPTH_24_BIT,
                  full_screen=True)
