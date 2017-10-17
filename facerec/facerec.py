import cv2
import os
import numpy as np


class FacialRecognition(object):
    camera_port = None
    ramp_frames = None
    camera = None
    subjects = None
    face_recognizer = None

    def __init__(self):
        self.camera_port = 0  # Index to camera port
        self.ramp_frames = 30  # Number of frames to throw away while the camera adjusts to light levels
        self.camera = cv2.VideoCapture(self.camera_port)  # Setting camera to the given camera port
        self.subjects = ["", "Erlend Helgerud", "Elvis Presley", "Random"]
        print("Preparing data...")
        faces, labels = self.prepare_training_data("training-data")
        print("Data prepared")
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.train(faces, np.array(labels))

    # Function to capture image from camera
    def get_image(self):
        retval, im = self.camera.read()
        return im

    # Function to detect faces using OpenCV
    @staticmethod
    def detect_face(img):
        # Convert the test image to gray image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load OpenCV LBP face-detector
        face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
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
                # Read image
                image = cv2.imread(image_path)

                # Display a window to show the image
                # cv2.imshow('Training on image...', image)
                # cv2.waitKey(100)
                # Detect face
                face, rect = self.detect_face(image)

                if face is not None:
                    # Add face to the list of faces
                    faces.append(face)
                    # Add label to the list of labels
                    labels.append(label)
        # cv2.destroyAllWindows()
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()

        return faces, labels

    # Function to draw rectangle on image according to given (x, y)
    # coordinates and given width and height
    # CURRENTLY UNUSED
    @staticmethod
    def draw_rectangle(img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Function to draw text on given image starting from passed (x, y) coordinates.
    # CURRENTLY UNUSED
    @staticmethod
    def draw_text(img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    # This function recognizes the person in image passed and draws a
    # rectangle around detected face with name of the subject
    def predict(self):
        found = False
        while found is not True:
            for i in range(self.ramp_frames):
                temp = self.get_image()
            print('Identifying ...')
            camera_capture = self.get_image()
            file = "reference-data/reference.png"
            cv2.imwrite(file, camera_capture)
            img = cv2.imread("reference-data/reference.png")
            # Detect face from given image
            face, rect = self.detect_face(img)

            # Check if a face is detected
            if face is not None:
                # Predict the face using face recognizer
                label = self.face_recognizer.predict(face)
                if label[1] < 60:
                    label_text = self.subjects[label[0]]
                    print(label_text)
                    print(label[1])
                    found = True
                else:
                    print('Unknown')
                    print(label[1])
                # Get name of respective label returned by face recognizer
            else:
                print('Unknown')

                # Draw a rectangle around face detected
                # draw_rectangle(img, rect)
                # Write name of predicted person
                # draw_text(img, label_text, rect[0], rect[1] - 5)


#perform a prediction
#predict()

#display both images
# cv2.imshow("Tom cruise test", predicted_img1)
# cv2.imshow("Shahrukh Khan test", predicted_img2)
# cv2.imshow("Shahrukh Khan", predicted_img3)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
