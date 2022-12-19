import base64

import cv2
import face_recognition
import numpy as np


def encode(image):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")

    # extract the person name from the image path
    print("[INFO] processing image")
    jpg_original = base64.b64decode(image)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)

    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imdecode(jpg_as_np, flags=1)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model="hog")

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    return encodings
