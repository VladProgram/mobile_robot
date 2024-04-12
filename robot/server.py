import os
import cv2
import requests
import time
from flask import Flask, jsonify, render_template, request, url_for, Response
from waitress import serve

from robot.tools.cam import *
from robot.tools.serial import *


cam = CameraDaemon()
com = SerialDummy()

app = Flask(__name__)

@app.route('/frame')
def frame():
  # return Response(cam.read_buf(), mimetype='multipart/x-mixed-replace; boundary=frame')
  return Response(cam.read_buf(), mimetype='image/jpeg')


@app.route('/command')
def command():
  data = request.args.to_dict()
  print(data)
  if "move" in data:
    com.send(data["move"])
  return jsonify(data)


if __name__ == '__main__':
  # cam.start()

  serve(app, host='0.0.0.0', port=9901)

  cam.close()
  ser.close()