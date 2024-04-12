import os
import cv2
import time

from robot.tools.daemon import *


class CameraDaemon(DaemonBase):
  def __init__(self, cam_id=0, period=1, path="/dev/shm/frame.jpg"):
    super().__init__(period=period)
    self.path = path
    self.frame = None
    self.cap = cv2.VideoCapture(cam_id)
    print(type(self).__name__, cam_id, "warming...")
    time.sleep(1)

  def close(self):
    self.cap.close()

  def read(self):
    ret, self.frame = self.cap.read()
    if ret:
      return self.frame
    else:
      print(type(self).__name__, "error")
      return None

  def read_buf(self):
    frame = self.read()
    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

  def loop(self):
    frame = self.read()
    if frame:
      cv2.imwrite(self.path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
