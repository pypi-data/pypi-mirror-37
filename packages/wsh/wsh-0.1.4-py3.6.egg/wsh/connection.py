"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""

import json
import click
import websocket
from blinker import signal
from prompt_toolkit.document import Document


class Connection:

    def __init__(self, ws_url, app, debug=True):
        signal('wsh-send').connect(self.send)
        signal('wsh-close').connect(self.close)
        self.ws_url = ws_url
        self.app = app
        self.output = app.layout.container.children[0].content.buffer
        self.ws = websocket.WebSocketApp(ws_url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)
        self.ws.run_forever(ping_interval=30)

    def display(self, string, direction=None):
        """Outputs the given string to the UI."""
        if direction is None:
            cursor = ''
        elif direction == 'in':
            cursor = '<<< '
        elif direction == 'out':
            cursor = '>>> '
        output = self.output.text + u'\n' + cursor + string
        self.output.document = Document(text=output, cursor_position=len(output))

    def info(self, string):
        """Output given string as info, which is a right justified text element."""
        width = click.get_terminal_size()[0]
        output = string.rjust(width)
        output = self.output.text + '\n' + output
        self.output.document = Document(text=output, cursor_position=len(output))

    def send(self, sender, **kw):
        """Send a data payload to the server."""
        data = kw['data']
        self.ws.send(data)
        try:
            json_data = json.loads(data)
            self.display('sent', direction='out')
            self.display(json.dumps(json_data, indent=2))
        except Exception:
            self.display('sent', direction='out')
            self.display(data)

    def close(self, sender, **kw):
        """Close connection to the server."""
        self.ws.close()

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            self.display('received', direction='in')
            self.display(json.dumps(data, indent=2))
        except Exception:
            self.display('received', direction='in')
            self.display(message.decode('utf-8'))

    def on_error(self, ws, error):
        message = "Error occured during connection to ({})".format(self.ws_url)
        self.info(message)
        self.info(str(error))

    def on_close(self, ws):
        self.info('Connection closed with ("{}")'.format(self.ws_url))

    def on_open(self, ws):
        self.info('Connection opened with ("{}")'.format(self.ws_url))
