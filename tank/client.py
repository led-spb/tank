import socket


class Tank:
    def __init__(self, host, port=8300):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        pass

    def command(self, cmd, *args):
        params = " ".join([str(x) for x in args])
        self.sock.sendall(f'{cmd}: {params}'.encode('utf-8'))
        return self.sock.recv(1024).decode('utf-8')

    def motor(self, left: int, right: int) -> None:
        self.command('motor', left, right)
