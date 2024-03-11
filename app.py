import sys
import os
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin

from wasteDectection.pipeline.training_pipeline import TrainPipeline
from wasteDectection.utils.main_utils import decodeImage, encodeImageIntoBase64
from wasteDectection.constant.application import APP_HOST, APP_PORT

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

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
        image = request.json.get('image')
        if not image:
            return Response("No image data found", status=400)

        decodeImage(image, clApp.filename)

        os.system("cd yolov5/ && python detect.py --weights beast.pt --img 416 --conf 0.5 --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov5/runs")

        # Read the output file of object detection and determine the objects detected
        with open("yolov5/runs/detect/exp/output.txt", "r") as file:
            detected_objects = file.read()

        # Prepare result message based on detected objects
        result_message = "Objects detected: " + detected_objects

        return jsonify(result_message)

    except Exception as e:
        print(e)
        return Response("An error occurred while processing the request", status=500)

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

        # Prepare result message based on detected objects
        result_message = "Objects detected: " + detected_objects

        return jsonify(result_message)

    except Exception as e:
        print(e)
        return Response("An error occurred while processing the request", status=500)

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host=APP_HOST, port=APP_PORT)

