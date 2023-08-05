#!/usr/bin/env python3
"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""

import click
import _thread as thread
from .connection import Connection
from .app import app, command_processor


class WSH:

    def __init__(self, host, commands=None):
        self.host = host
        if commands:
            for key, value in commands.items():
                command_processor.register_command(key, value)

    def run(self):
        def connection():
            Connection(self.host, app)
        thread.start_new_thread(connection, ())
        app.run()


@click.command()
@click.argument('host')
def wsh(host):
    WSH(host).run()


if __name__ == '__main__':
    wsh()
