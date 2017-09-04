# By Erlend Helgerud
# Code reworked from https://github.com/noahingham/face-recognition-python

import cv2, sys, numpy, os


class FacialRecognition(object):
    size = 1
    fn_haar = 'haarcascade_frontalface_default.xml'
    fn_dir = 'att_faces'

    (dirs, subdirs, files) = (None, None, None)
    (images, labels, names, id) = ([], [], {}, None)
    (image_width, image_height) = (112, 92)

    model = cv2.face.FisherFaceRecognizer_create()
    haar_cascade = cv2.CascadeClassifier(fn_haar)
    webcam = cv2.VideoCapture(0)

    (frame, gray, faces) = (None, None, None)

    def __init__(self):
        self.initialize()
        self.model.train(self.images, self.labels)
        self.webcam = cv2.VideoCapture(0)

    def initialize(self):
        id = 0
        self.id = id
        for subdirs, dirs, files in os.walk(self.fn_dir):
            for subdir in dirs:
                self.names[self.id] = subdir
                subjectpath = os.path.join(self.fn_dir, subdir)
                for filename in os.listdir(subjectpath):
                    f_name, f_extension = os.path.splitext(filename)
                    if (f_extension.lower() not in
                            ['.png', '.jpg', '.jpeg', '.gif', '.pgm']):
                        print('Skipping ' + filename + ', wrong type')
                        continue

                    path = subjectpath + '/' + filename
                    label = self.id

                    self.images.append(cv2.imread(path, 0))
                    self.labels.append(int(label))

                self.id += 1

            (self.images, self.labels) = [numpy.array(lis) for lis in [self.images, self.labels]]

    def start_cam(self):
        rval = False
        while not rval:
            (rval, self.frame) = self.webcam.read()
            if not rval:
                print('Failed to open webcam, trying again...')
        # TODO REMOVE
        self.frame = cv2.flip(self.frame, 1, 0)
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        mini = cv2.resize(self.gray, (int(self.gray.shape[1] / self.size), int(self.gray.shape[0] / self.size)))
        self.faces = self.haar_cascade.detectMultiScale(mini)

    def train(self, fn_name):
        count = 0
        pause = 0
        count_max = 30

        if fn_name != '' or fn_name is not None:
            path = os.path.join(self.fn_dir, fn_name)
            if not os.path.isdir(path):
                os.mkdir(path)

        pin = sorted([int(n[:n.find('.')]) for n in os.listdir(path)
                      if n[0] != '.'] + [0])[-1] + 1

        print("\n\033[94mThe program will save 30 samples. Move your head around to increase while it runs.\033[0m\n")
        while count < count_max:
            self.start_cam()
            height, width, channels = self.frame.shape
            self.faces = sorted(self.faces, key=lambda x: x[3])

            if self.faces:
                face_i = self.faces[0]
                (x, y, w, h) = [v * self.size for v in face_i]

                face = self.gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.image_width, self.image_height))

                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(self.frame, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
                            1, (0, 255, 0))
                if w * 6 < width or h * 6 < height:
                    print('Face to small')
                else:
                    if pause == 0:
                        print('Saving training sample ' +
                              str(count + 1) + '/' + str(count_max))
                        cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
                        pin += 1
                        count += 1
                        pause = 1
            if pause > 0:
                pause = (pause + 1) % 5
            cv2.imshow('OpenCV', self.frame)
            key = cv2.waitKey(10)

    def predict_face(self):
        self.start_cam()
        for i in range(len(self.faces)):
            face_i = self.faces[i]
            (x, y, w, h) = [v * self.size for v in face_i]
            face = self.gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (self.image_width, self.image_height))

            prediction = self.model.predict(face_resize)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1] < 700:
                print(self.names[prediction[0]])
                cv2.putText(self.frame,
                            '%s - %.0f' % (self.names[prediction[0]], prediction[1]),
                            (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                print('Unknown')
                cv2.putText(self.frame,
                            'Unknown',
                            (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow('OpenCV', self.frame)
        key = cv2.waitKey(10)