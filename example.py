import time

from tank.client import Tank

client = Tank('192.168.168.8')
client.motor(-4095, 4095)
time.sleep(1)
client.motor(0, 0)
