import socket


class Tank:
    def __init__(self, host, port=8300):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        pass

    def command(self, cmd, *args):
        params = " ".join([str(x) for x in args])
        self.sock.sendall(f'{cmd}: {params}'.encode('utf-8'))
        response = self.sock.recv(1024).decode('utf-8').strip()

        parts = response.split(':', 1)
        if len(parts) != 2:
            raise RuntimeError(f'Invalid response from server: {response}')
        if parts[0] == 'err':
            raise RuntimeError(f'Error from server: {parts[1]}')

        if parts[1] == '':
            return None
        try:
            return int(parts[1])
        except ValueError:
            try:
                return float(parts[1])
            except ValueError:
                pass
        return parts[1]

    def motor(self, left: int, right: int) -> None:
        self.command('motor', left, right)

    def distance(self) -> float:
        return self.command('distance')
