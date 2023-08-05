.. |pypi| image:: https://img.shields.io/pypi/v/wsh.svg?style=flat-square
    :target: https://pypi.python.org/pypi/wsh
.. |license| image:: https://img.shields.io/pypi/l/wsh.svg?style=flat-square
    :target: https://pypi.python.org/pypi/wsh

****
WSH
****
|pypi| |license| 

WSH is a command line interface that launches a shell to send and recieve
messages from a WebSocket server. It was designed to be simplistic and allow
developers to easily connect/send/receive data over a WS with very little effort.

Quickstart
==========

Install via PyPi:

.. code-block:: shell

    pip install wsh


Then simply call the command line tool with your WebSocket server host, you should
also specify the WebSocket protocol ("ws" or "wss")

.. code-block:: shell

    wsh ws://127.0.0.1:7001/ws/connection


For more complex scenarios you can launch the shell manually via a simple python script.

.. code-block:: python

     from wsh import WSH


     def main():
         # Custom Logic
         # ............
         wsh = WSH(host='ws://127.0.0.1:7001/ws/connection')
         wsh.run()


     if __name__ == '__main__':
         main()

