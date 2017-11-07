import cv2


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
        else:
            pass


