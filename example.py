import time

from tank.client import Tank

client = Tank('192.168.168.8')
print(client.distance())

#client.motor(-4000, -4000)
#time.sleep(1)
#client.motor(0, 0)
