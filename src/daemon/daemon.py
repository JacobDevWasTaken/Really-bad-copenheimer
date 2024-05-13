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


def handle_connection(sock: socket.socket):
    global running
    global discover_process
    if running:
        inp: str = sock.recv(4096).decode("UTF-8")
        if inp:
            args: list[str] = inp.lower().split()
            if args[0] == "help":
                sendx(sock, "Usage: [discover | rescan | interface | stop-daemon | db] [OPTIONS]")
                sendx(sock, "Type one of the above to show more info about it.")
                sendx(sock, "For more info, please refer to https://github.com/JacobborstellCoder/Horrible_copenheimer")
            elif args[0] == "discover":
                if len(args) == 1:
                    sendx(sock, "Usage: discover [start | stop | restart | config] [OPTIONS]")
                    sendx(sock, "Controls the server scanner. Start it with \"discover start\".")
                elif len(args) == 2:
                    if args[1] == "start":
                        discover(True)
                    if args[1] == "stop":
                        discover(False)
            elif args[0] == "rescan":
                if len(args) == 1:
                    sendx(sock, "Usage: rescan [start | stop | restart | config] [OPTIONS]")
                    sendx(sock, "Controls the rescanner. Start it with \"rescan start\".")
            elif args[0] == "interface":
                if len(args) == 1:
                    sendx(sock, "Usage: interface [help | config | reload-config] [OPTIONS]")
                    sendx(sock,
                          "Allows you to configure the user interface settings. For more info, type \"interface help\".")
            elif args[0] == "stop-daemon":
                running = False
                ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ss.connect((load_interface_config("CLI.Host"), load_interface_config("CLI.Port")))
                ss.close()
                sendx(sock, "!CLOSE_CONNECTION")
            else:
                sendx(sock, "Unknown command.")

    sock.close()


def start():
    global running

    print("Starting daemon...")
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
