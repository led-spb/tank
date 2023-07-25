import logging
import socketserver
import time
from core.Motor import PWM


class CommandHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        try:
            while(True):
                data = self.request.recv(1024).strip()
                if len(data) == 0:
                    return

                try:
                    command = bytes.decode(data, encoding="utf-8")

                    cmd, params = command.split(':', 1)
                    params = params.strip().split(' ')
                    logging.debug(f'{cmd} {params}')

                    self.execute_command(cmd, params)
                except RuntimeError:
                     logging.exception('Error while executing command')
                self.request.sendall('ok'.encode('utf-8'))
        finally:
            PWM.setMotorModel(0, 0)

    def execute_command(self, command, params):
        if command == 'motor':
            left = int(params[0])
            right = int(params[1])
            logging.debug(f'{left} {right}')
            PWM.setMotorModel(int(params[0]), int(params[1]))
        else:
            logging.error(f'Unknown command: {command}')
        return


class Server(socketserver.TCPServer):
    def __init__(self, port=8300 ):
        super().__init__(('0.0.0.0', port), CommandHandler)
        self.allow_reuse_address = True

    def run(self):
        try:
            self.serve_forever()
        finally:
            PWM.setMotorModel(0, 0)    
            self.server_close()
        pass


if __name__ == '__main__':
    logging.basicConfig(
        format=u'%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
        level=logging.DEBUG
    )

    server = Server()
    server.run()
