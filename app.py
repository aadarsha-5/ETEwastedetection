import sys
import os
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
import serial

from wasteDectection.pipeline.training_pipeline import TrainPipeline
from wasteDectection.utils.main_utils import decodeImage, encodeImageIntoBase64
from wasteDectection.constant.application import APP_HOST, APP_PORT

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

arduino_communication = serial.Serial('COM5', 9600, timeout=1)  # Replace 'COM1' with your Arduino's serial port

def send_command_with_ack(command):
    arduino_communication.write(command.encode())  # Send command to Arduino
    response = arduino_communication.readline().strip()  # Read response from Arduino
    return response == b'ACK'  # Check for acknowledgment

@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successful!!" 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

        os.system("cd yolov5/ && python detect.py --weights beast.pt --img 416 --conf 0.5 --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov5/runs")

        # Read the output file of object detection and determine the objects detected
        with open("yolov5/runs/detect/exp/output.txt", "r") as file:
            detected_objects = file.read()

        # Determine whether to send the signal based on detected objects
        if "Biodegradable" in detected_objects:
            command = "B"  # Signal to send for biodegradable objects
            message = "Biodegradable object detected"
        elif "Nonbiodegradable" in detected_objects:
            command = "N"  # Signal to send for non-biodegradable objects
            message = "Non-biodegradable object detected"
        else:
            command = "U"  # Signal to send for unknown objects
            message = "Unknown object detected"

        # Send command to Arduino with acknowledgment
        success = send_command_with_ack(command)

        if success:
            print(f"{message} - Signal sent: {command}")
            return jsonify(result)
        else:
            return Response("Failed to receive acknowledgment from Arduino")

    except ValueError as val:
        print(val)
        return Response("Value not found inside json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"
        return jsonify(result)

@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        # Perform object detection in real-time
        os.system("cd yolov5/ && python detect.py --weights beast.pt --img 416 --conf 0.5 --source 0")
        os.system("rm -rf yolov5/runs")

        # Read the output file of object detection and determine the objects detected
        with open("yolov5/runs/detect/exp/output.txt", "r") as file:
            detected_objects = file.read()

        # Determine whether to send the signal based on detected objects
        if "Biodegradable" in detected_objects:
            command = "B"  # Signal to send for biodegradable objects
            message = "Biodegradable object detected"
        elif "Nonbiodegradable" in detected_objects:
            command = "N"  # Signal to send for non-biodegradable objects
            message = "Non-biodegradable object detected"
        else:
            command = "U"  # Signal to send for unknown objects
            message = "Unknown object detected"

        # Send command to Arduino with acknowledgment
        success = send_command_with_ack(command)

        if success:
            print(f"{message} - Signal sent: {command}")
            return "Camera starting!!"
        else:
            return Response("Failed to receive acknowledgment from Arduino")

    except ValueError as val:
        print(val)
        return Response("Value not found inside json data")
    except Exception as e:
        print(e)
        return Response("Error during live detection and sending command to Arduino")

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host=APP_HOST, port=APP_PORT)
