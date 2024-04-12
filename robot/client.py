import cv2
import requests
import numpy as np
import time


from robot.tools.daemon import *


class RobotDummyCommandsDaemon(DaemonBase):
  def __init__(self, period=3):
    super().__init__(period=period)
    self.idx = 0
    self.move = ['F', 'F', 'R', 'F', 'R', 'F', 'F', 'R', 'F', 'R', 'F', 'F']

  def loop(self):
    response = requests.get('http://127.0.0.1:9901/command', params={'move': self.move[self.idx]})
    if response.status_code == 200:
      print(type(self).__name__, "Command sent successfully", response.content)
    else:
      print(type(self).__name__, "Failed to send command to server")

    self.idx += 1
    if self.idx >= len(self.move):
      self.idx = 0


def show_image_from_server():
  while(True):
    response = requests.get('http://127.0.0.1:9901/frame', stream=True)
    if response.status_code == 200:
      try:
        image_array = np.frombuffer(response.content, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is not None:
          cv2.imshow('Frame', image)
          cv2.waitKey(1)
        else:
          print("Failed to decode image from server")
      except Exception as e:
        print("Error decoding image:", e)
    else:
      print("Failed to fetch frame from server")
    time.sleep(0.1)


if __name__ == "__main__":
  cmd = RobotDummyCommandsDaemon(period=1)
  cmd.start()

  show_image_from_server()
