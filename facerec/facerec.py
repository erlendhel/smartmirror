import os

import cv2
import numpy as np

import singletonCamera
from db import smartmirrordb
from timer_module import time_module


# Tested and compatible with Raspberry Pi 3 and PiCam. Additional setup to get
# OpenCV to work on Raspberry Pi 3 is needed.


# Class used to perform facial recognition on the smartmirror. 
# Used to differentiate between users of the smartmirror. The code
# does support the addition of users, but this will have to be done
# manually. The face-recognition is based in the OpenCV Library, and
# uses the LBPH-algorithm for recognition (Local Binary Patterns Histogram.
# The choice of algorithm is based on the effectiveness of LBPH compared
# to Eigenfaces or FisherFaces. Since the program is run on RP3, this is 
# a big concern. Additionally, LBPH is less sensitive to light, which suits
# the use cases of the smartmirror. Additionally, to increase the effectiveness
# of the facial-recognition, the script takes a picture, stores it to file, and
# processes it, instead of doing a realtime facial-recognition.
#
# NOTE:
# After setting up OpenCV, the command 'sudo modprobe bcm2835-v4l2' must be written
# in the commandline.
class FacialRecognition(object):
    ramp_frames = None
    camera = None
    subjects = None
    face_recognizer = None
    db = None
    timer = None

    def __init__(self):
        self.timer = time_module.Timer()
        self.db = smartmirrordb.UserDB()
        # Number of frames to throw away while the camera adjusts to light levels
        self.ramp_frames = 30
        self.camera = singletonCamera.Camera().instance.camera

        # List of names of the predefined users.
        #
        # NOTE:
        # The list of subject names MUST be coherent with the indexing of
        # images provided in the 'training-data' folder. Since there is
        # no 0'th index of folders (no s1), the space is left blank. The
        # rest of the indexes are linked to s1, s2, s3 etc.
        self.subjects = [""]
        ids = self.db.get_all_ids()
        for id in ids:
            self.subjects.append(id)
        print("Preparing data...")

        # 'prepare_training_data' produces two vectors, one for images,
        # and one for labels. Labels are integers from one and up, which
        # represent the index of the list 'subjects'.

        dir = ""
        if __name__ == '__main__':
            dir = "training-data"
        else:
            dir = "facerec/training-data"

        faces, labels = self.prepare_training_data(dir)

        print("Data prepared")
        # Create the LBPH face-recognizer
        #
        # NOTE:
        # If algorithm is changed, this has to be changehd aswell.
        self.face_recognizer = cv2.face.createLBPHFaceRecognizer()
        # Training face-recognizer with the face-vectors and label-vectors
        # generated by 'prepare_training_data'.
        self.face_recognizer.train(faces, np.array(labels))

    # Function to capture image from camera
    def get_image(self):
        retval, im = self.camera.read()
        return im

    # Function to detect faces using OpenCV LBP face detector. 
    @staticmethod
    def detect_face(img):
        # Convert the test image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load OpenCV LBP face-detector
        #
        # NOTE:
        # If algorithm is changed, this needs to be changed aswell
        dir = ""
        if __name__ == '__main__':
            dir = "opencv-files/lbpcascade_frontalface.xml"
        else:
            dir = "facerec/opencv-files/lbpcascade_frontalface.xml" 

        face_cascade = cv2.CascadeClassifier(dir)

        # Detecting multiscale images
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        if len(faces) == 0:
            return None, None

        (x, y, w, h) = faces[0]

        return gray[y:y + w, x:x + h], faces[0]

    def prepare_training_data(self, data_folder_path):
        # Get directories in data folder
        dirs = os.listdir(data_folder_path)
        # List to hold all subject faces
        faces = []
        # List to hold labels for all subjects
        labels = []

        # Iterating through each directory and read images within it
        for dir_name in dirs:
            if not dir_name.startswith('s'):
                continue
            # Extract label number of subject from dir_name
            # Current format of dir_name = slabel
            label = int(dir_name.replace('s', ''))
            # Build path of directory containing images for current subject
            subject_dir_path = data_folder_path + '/' + dir_name
            # Get the names of images inside the given subject directory
            subject_image_names = os.listdir(subject_dir_path)

            # Iterate through each image name, read image
            # Detect a particular face and add face to list of faces
            for image_name in subject_image_names:
                # Ignore system files
                if image_name.startswith('.'):
                    continue

                # Build image path
                image_path = subject_dir_path + '/' + image_name
                # Read image from the given path in 'image_path'
                image = cv2.imread(image_path)

                # Detect face
                face, rect = self.detect_face(image)

                if face is not None:
                    # Add face to the list of faces
                    faces.append(face)
                    # Add label to the list of labels
                    labels.append(label)

        return faces, labels

    # This function recognizes the person in image passed
    def predict(self):
        # Set the timer to 0 and declare the end_time variable which will be added to for each iteration
        self.timer.restart()
        end_time = 0
        # Iterate until an accurate prediction is made, or until the timer runs above 10 seconds.
        while True:
            # Break the loop if timer runs over 10 and return false to indicate a timeout
            if end_time >= 10:
                return False
            for i in range(self.ramp_frames):
                temp = self.get_image()
            print('Identifying ...')
            # Get an image from the camera
            camera_capture = self.get_image()
            # Set the destination for the image, there will always just be one reference image.
            # This image is overwritten the next time a prediction must be made.
            file = ""
            if __name__ == '__main__':
                file = "reference-data/reference.png"
            else:
                file = "facerec/reference-data/reference.png"
            # Write the image to the path given in 'file'.
            cv2.imwrite(file, camera_capture)

            # Assign the appropriate path to dir in order to save the reference image
            dir = ""
            if __name__ == '__main__':
                dir = "reference-data/reference.png"
            else:
                dir = "facerec/reference-data/reference.png"
            
            # Read the image stored in the path given in 'file'
            img = cv2.imread(dir)
            
            # Detect face from given image
            face, rect = self.detect_face(img)

            # Check if a face is detected
            if face is not None:
                # Predict the face using face recognizer
                label = self.face_recognizer.predict(face)
                # The 'predict' function of face_recognizer returns two labels: label[0] contains a index number, the
                # float given in label[1] gives a reference number of how successful the prediction is. A lower
                # number indicates a more accurate prediction. Checking if a prediction is below 60 in order to
                # 'log in' a person.
                if label[1] < 60:
                    label_text = self.subjects[label[0]]
                    print('Facerec module found face with id: ', label_text)
                    print('Facerec accuracy:', label[1])
                    return label_text
                else:
                    print('Unknown')
                    # Add the passed time to the end_time variable
                    end_time = self.timer.get_time_in_seconds()
                # Get name of respective label returned by face recognizer
            else:
                print('Unknown')
                # Add the passed time to the end_time variable
                end_time = self.timer.get_time_in_seconds()
