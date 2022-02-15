import sys

import cv2

from local_detector import ObjectDetector
from local_detector import ObjectDetectorOptions

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os

# Setup for Azure Cognitive Services vision client
# Code can be found here:  https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/image-analysis-client-library?tabs=visual-studio&pivots=programming-language-python
subscription_key = "********************************"
endpoint = "https://cs437visionservice.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
local_image_path_objects = os.path.join (images_folder, "objects.jpg")

#Setup for OpenCV
camera_id = 0
height = 480
width = 640

# Initialize the TensorFlow Lite object detection model
# Code was adapted from https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi
options = ObjectDetectorOptions(
    num_threads=4,
    score_threshold=0.3,
    max_results=3,
    enable_edgetpu=0)
detector = ObjectDetector(model_path='efficientdet_lite0.tflite', options=options)

speed = 1

def detect_labels(use_local=True):

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

      # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        image = cv2.flip(image, -1)

        if use_local:
            labels = local_detector(image)
        else:
            cv2.imwrite(local_image_path_objects,image)
            labels = remote_detector()

        if 'stop sign' in labels:
            return True
        else:
            return False
    
    cap.release()

def local_detector(image):
    detections = detector.detect(image)

    labels = []

    for detection in detections:
        category = detection.categories[0]
        labels.append(category.label.lower())
        print(category.label)

    return labels

def remote_detector():
    local_image_objects = open(local_image_path_objects, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)
    
    labels = []
    
    for object in detect_objects_results_local.objects:
        labels.append(object.object_property)
        print(object.object_property)

    return labels

if __name__ == '__main__':
  detect_labels(use_local=False)