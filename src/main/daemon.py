"""
Really-Bad-Copenheimer
Copyright (C) <2024>  <Jacob Borstell>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from src.configloader import load_interface_config
import src.discover.main

running = True

discover_process: multiprocessing.Process = None


def sendx(soc: socket.socket, dat: str):
    soc.sendall((dat + "\n").encode("UTF-8"))


def discover(status: bool) -> str:
    global discover_process
    if status:
        if not discover_process:
            discover_process = multiprocessing.Process(target=src.discover.main.main)
            discover_process.start()
            return "Started the server scanner"
        else:
            return "The server scanner is already running"

    else:
        if discover_process:
            discover_process.terminate()
            discover_process = None
            return "Stopped the server scanner"
        else:
            return "The server scanner isn't running"

def handle_input(txt):
    global running
    global discover_process
    if running:
        if txt:
            args: list[str] = txt.lower().split()
            if args[0] == "help":
                return """
    Usage: [discover | rescan | process | db] [OPTIONS]"
    Type one of the above to show more info about it.
    For more info, please refer to https://github.com/JacobborstellCoder/Really-bad-copenheimer
    """

            elif args[0] == "discover":
                if len(args) == 1:
                    return """
    Usage: discover [start | stop | restart | config] [OPTIONS]
    Controls the server scanner. Start it with \"discover start\".
    """
                elif len(args) == 2:
                    if args[1] == "start":
                        return discover(True)
                    elif args[1] == "stop":
                        return discover(False)
                    elif args[1] == "restart":
                        return discover(False) + discover(True)


            elif args[0] == "rescan":
                if len(args) == 1:
                    return """
    Usage: rescan [start | stop | restart | config] [OPTIONS]
    Controls the rescanner. Start it with \"rescan start\".
    """


            elif args[0] == "stop":
                running = False
                return "!CLOSE_CONNECTION"
            else:
                return "Unknown command."

def handle_connection(sock: socket.socket):
    

    sock.close()


def start():
    global running

    print("Starting main...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.bind((load_interface_config("CLI.Host"), load_interface_config("CLI.Port")))
        soc.listen()
    except OSError as e:
        print("An error occurred:", e)
    print("Listening at " + load_interface_config("CLI.Host") + ":" + str(load_interface_config("CLI.Port")))

    with ThreadPoolExecutor(max_workers=load_interface_config("CLI.MaxConnections")) as pool:
        while running:
            conn, addr = soc.accept()
            pool.submit(handle_connection, conn)
    soc.close()
    discover(False)
