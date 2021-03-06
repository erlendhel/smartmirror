import os
import cv2
import singletonCamera
from db import smartmirrordb

# Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
camera = singletonCamera.Camera().instance.camera
db = smartmirrordb.UserDB()


# Function to capture image from camera
def get_image():
    retval, im = camera.read()
    return im


# Function to add a user face to the user database of the smartmirror
def add_face(id):
    print('Taking image..')  # TODO: Delete?
    n = 1
    if __name__ == '__main__':
        if not os.path.isdir("training-data/s" + str(id)):
            os.mkdir("training-data/s" + str(id))
        return_path = "training-data/s" + str(id)
    else:
        if not os.path.isdir("facerec/training-data/s" + str(id)):
            os.mkdir("facerec/training-data/s" + str(id))
        return_path = "facerec/training-data/s" + str(id)
    while n < 45:
        print('Taking image')
        camera_capture = get_image()
        if __name__ == '__main__':
            file = "training-data/s" + str(id) + "/" + str(n) + ".png"
        else:
            file = "facerec/training-data/s" + str(id) + "/" + str(n) + ".png"

        cv2.imwrite(file, camera_capture)
        n = n + 1

    return return_path
