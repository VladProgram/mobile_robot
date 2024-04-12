import cv2
import requests
import numpy as np
import time


from robot.tools.daemon import *
from robot.tools.openai import *


class BaseRobotCommandsDaemon(DaemonBase):
  def __init__(self, ip, period=1):
    super().__init__(period=period)
    self.url_base = f"http://{ip}:9901"
    self.url_frame = f"{self.url_base}/frame"
    self.url_command = f"{self.url_base}/command"
    self.frame = None
    print(type(self).__name__, "init", self.url_base)

  def play(self):
    if self.frame is not None:
      cv2.imshow('Frame', self.frame)
      cv2.waitKey(1)


class RobotDummyCommandsDaemon(BaseRobotCommandsDaemon):
  def __init__(self, ip, period=3):
    super().__init__(ip, period)
    self.idx = 0
    self.move = ['F', 'F', 'R', 'F', 'R', 'F', 'F', 'R', 'F', 'R', 'F', 'F']

  def loop(self):
    response = requests.get(self.url_command, params={'move': self.move[self.idx]})
    if response.status_code == 200:
      print(type(self).__name__, "Command sent successfully", response.content)
    else:
      print(type(self).__name__, "Failed to send command to server")

    self.idx += 1
    if self.idx >= len(self.move):
      self.idx = 0


class RobotCommandsDaemon(BaseRobotCommandsDaemon):
  def __init__(self, ip, period=1):
    super().__init__(ip, period)
    self.model = DummyPredictor()

  def read_frame(self):
    response = requests.get(self.url_frame, stream=True)
    if response.status_code == 200:
      try:
        image_array = np.frombuffer(response.content, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
      except Exception as e:
        print(type(self).__name__, "Error decoding image:", e)
    else:
      print(type(self).__name__, "Failed to fetch frame from server")

  def loop(self):
    self.frame = self.read_frame()

    prediction = self.model.predict(self.frame)
    print(type(self).__name__, "prediction", prediction)


if __name__ == "__main__":
  cmd = RobotCommandsDaemon(ip="127.0.0.1", period=0.1)
  cmd.start()

  cmdt = RobotDummyCommandsDaemon(ip="127.0.0.1", period=3)
  cmdt.start()

  while(True):
    cmd.play()
    time.sleep(0.1)
