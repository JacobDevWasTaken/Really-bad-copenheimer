import threading

import src.configloader

import src.discover.port_scanner.workerSimple
import src.discover.port_scanner.workerAsyncio
import src.discover.port_scanner.workerNonBlockingSockets

GREEN = "\033[1;32;48m"
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
END = "\033[1;37;0m"


def main():
    port_scanner_mode = src.configloader.load_discover_config("Portscanner.Mode")

    def logger(ip, port):
        print("Found open port: " + ip + ":" + str(port))

    func = None

    if port_scanner_mode == "SimpleThreaded":
        pass

    elif port_scanner_mode == "AsyncioBatchThreaded":
        func = src.discover.port_scanner.workerAsyncio.run_worker

    elif port_scanner_mode == "NonBlockingSocketsThreaded":
        func = src.discover.port_scanner.workerNonBlockingSockets.run_worker

    if func:
        for i in range(src.configloader.load_discover_config("Portscanner.Threads")):
            th_ = threading.Thread(target=func, args=(logger,))
            th_.start()
