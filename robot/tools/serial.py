import serial
import time


class SerialDummy:
  def __init__(self, address='/dev/ttyACM0', speed=9600):
    print(type(self).__name__, address, speed)

  def close(self):
    print(type(self).__name__)

  def send(self, value):
    print(type(self).__name__, "send", value)


class SerialCom:
  def __init__(self, address='/dev/ttyACM0', speed=9600):
    self.address = address
    self.speed = speed
    self.com = serial.Serial(self.address, self.speed)
    print(type(self).__name__, self.address, self.speed, "warming...")
    time.sleep(2)

  def close(self):
    self.com.close()

  def send(self, value):
    self.com.write(f"{value}\n".encode())