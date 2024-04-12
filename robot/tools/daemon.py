import threading
import time


class DaemonBase:
  def __init__(self, period=0):
    self.is_running = False
    self.is_started = False
    self.period = period

  def start(self):
    if self.is_started:
      print(type(self).__name__, "already started")
      return

    print(type(self).__name__, "Start")
    self.is_running = True
    self.is_started = True
    self.thread = threading.Thread(target = self.safe_run)
    self.thread.setDaemon(True)
    self.thread.start()

  def stop(self):
    print(type(self).__name__, "Stop")
    self.is_running = False

  def join(self):
    self.thread.join()

  def loop(self):
    pass

  def run(self):
    while(self.is_running):
      try:
        self.loop()
      except Exception as e:
        print(type(self).__name__, "Exception", e, "RUN")
      time.sleep(self.period)

  def safe_run(self):
    print(type(self).__name__, "RUN start")
    try:
      self.run()
    except Exception as e:
      print(type(self).__name__, "Exception", e, "safe_run")
    print(type(self).__name__, "RUN finished")
