import logging
import socketserver
from core.Motor import PWM
from core.Servo import servo
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
        for idx, param in enumerate(params):
            try:
                params[idx] = int(param)
            except ValueError:
                try:
                    params[idx] = float(param)
                except ValueError:
                    pass

        logging.debug(f'{command} params={params}')
        return command, params

    def execute_command(self, command, params):
        retval = None
        if command == 'motor':
            if len(params) != 2 or not isinstance(params[0], int) or not isinstance(params[1], int):
                raise RuntimeError('command needs 2 parameters: (int, int)')
            PWM.setMotorModel(params[0], params[1])
            retval = 0
        elif command == 'distance':
            retval = ultrasonic.get_distance()
        elif command == 'servo':
            if len(params) != 2 or not isinstance(params[0], int) or not isinstance(params[1], int):
                raise ValueError('command needs 2 parameters: (int, int)')
            servo.setServoPwm(str(params[0]), params[1])
            return 0
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
