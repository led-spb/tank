import logging
import socketserver
from core.Motor import PWM
from core.Ultrasonic import ultrasonic


class CommandHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        try:
            while True:
                data = self.request.recv(1024).strip()
                if len(data) == 0:
                    return

                try:
                    command = bytes.decode(data, encoding="utf-8")
                    cmd, params = self.parse_input_command(command)

                    retval = self.execute_command(cmd, params)
                    response = f'ok: {retval}'
                except BaseException as err:
                    logging.exception('Error while executing command')
                    response = f'err: {err}'

                self.request.sendall(response.encode('utf-8'))
        finally:
            PWM.setMotorModel(0, 0)

    def parse_input_command(self, data):
        parts = data.split(':', 1)
        if len(parts) < 2:
            raise ValueError('Malformed command')

        command = parts[0]
        params = parts[1].strip().split(' ')

        logging.debug(f'{command} params={params}')
        return command, params

    def execute_command(self, command, params):
        retval = None
        if command == 'motor':
            left = int(params[0])
            right = int(params[1])
            logging.debug(f'{left} {right}')
            PWM.setMotorModel(int(params[0]), int(params[1]))
            retval = 0
        elif command == 'distance':
            retval = ultrasonic.get_distance()
        else:
            raise RuntimeWarning(f'Unknown command: {command}')
        return retval


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
