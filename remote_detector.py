import cv2
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os

subscription_key = "********************************"
endpoint = "https://cs437visionservice.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    check, frame = cam.read()

    cv2.imshow('video', frame)


    local_image_path_objects = os.path.join (images_folder, "objects.jpg")
    cv2.imwrite(local_image_path_objects,frame)
    local_image_objects = open(local_image_path_objects, "rb")
    # Call API with local image
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)

    # Print results of detection with bounding boxes
    print("Detecting objects in local image:")
    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        for object in detect_objects_results_local.objects:
            print("{} at location {}, {}, {}, {}".format( object.object_property, \
            object.rectangle.x, object.rectangle.x + object.rectangle.w, \
            object.rectangle.y, object.rectangle.y + object.rectangle.h))
    print()

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()