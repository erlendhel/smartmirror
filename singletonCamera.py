import cv2


# The camera instance in the smartmirror-app is a singleton in order to control the behavior.
# Since multiple classes are dependent on the camera, and only one instance of the camera can
# exist at once, we opted for the singleton design.
class Camera(object):
    camera_port = None
    camera = None

    class __Camera:
        def __init__(self):
            self.camera_port = 0
            self.camera = cv2.VideoCapture(self.camera_port)
    instance = None

    def __init__(self):
        if not Camera.instance:
            Camera.instance = Camera.__Camera()


