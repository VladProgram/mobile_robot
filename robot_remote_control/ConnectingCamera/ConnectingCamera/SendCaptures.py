import cv2
import requests
import time

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        # Encode captures to JPEG
        quality = 80
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

        # Send captures for web server established by Raspberry pi
        response = requests.post(
            'http://127.0.0.1:9901/upload',
            files={'image': buffer.tobytes()}
        )
        print("Image uploaded")

    # Send duration (Second)
    time.sleep(1)

# Release resources
cap.release()
