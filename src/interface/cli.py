import socket
import time


def start(daemon_host: str = "127.0.0.1", daemon_port: int = 25250):
    print("Starting CLI...")
    print("Type \"help\" for more info.")
    while True:
        try:
            inp = input("Copenheimer > ").lower()
        except KeyboardInterrupt:
            return 0

        if inp:
            if (inp == "exit") or (inp == "quit"):
                return 0
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((daemon_host, daemon_port))
            except Exception:
                print("Could not connect to daemon at " + daemon_host + ":" + str(daemon_port))
                return 1

            sock.settimeout(1)

            sock.sendall(inp.encode("UTF-8"))
            time.sleep(0.1)
            fragments = []
            while True:
                try:
                    chunk = sock.recv(1024)
                except socket.timeout:
                    break
                if not chunk:
                    break
                fragments.append(chunk)

            if fragments:
                dat = (b''.join(fragments)).decode("UTF-8")
                if dat == "!CLOSE_CONNECTION\n":
                    sock.close()
                    return 0
                print(dat, end="")


if __name__ == "__main__":
    start()
