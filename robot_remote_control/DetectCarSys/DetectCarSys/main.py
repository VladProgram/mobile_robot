from flask import Flask, jsonify, render_template, request, url_for
import serial
import time
import os
from waitress import serve

#serial setting
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  

#flask(web server) setting 
app = Flask(__name__)

#define pass for captures from camera
UPLOAD_FOLDER = 'static/Capture'

#app.route() is flask style writing
#default setting of flask. rendering template from 'index.html'
@app.route('/')
def index():
    return render_template('index.html')

#route for sending buttom value for Arduino to operate moter
#receiving value from Web server's controller by json
@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()  
    button_value = data['button_value']
    print('Received value:', button_value)
    ser.write(f"{button_value}\n".encode())
    return jsonify({ 'value': button_value})

#route for uploading captures from camera
#save capture in folder and Web server read and show the capture
@app.route('/upload', methods=['POST'])
def upload_image():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, 'image.jpg')
    image.save(image_path)
    return url_for('static', filename='Capture/image.jpg')

#establish Web server
if __name__ == '__main__':
    #default flask server
    #app.run(debug=True, host = '0.0.0.0')

    #Web server by waitress
    serve(app, host='0.0.0.0', port=5000)

#program when stop running
if KeyboardInterrupt:
    ser.close()
    print("finish")