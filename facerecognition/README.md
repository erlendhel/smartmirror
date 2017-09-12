# Usage/Testing of facial recognition

#### Dependencies
##### Note:
The following imports are already imported in facerec.py, might require local setup to work
<pre><code>import cv2, sys, numpy, os
</pre></code>

Required import in main program:
<pre><code>from facerecognition import facerec
</pre></code>

Faces used in the facial recognition is stored in folder with path
<pre><code>att_faces/
</pre></code>

#### Create object of the FacialRecognition class
##### Code:
<pre><code>facerec = facerec.FacialRecognition()
</pre></code>

#### Train facial recognition
##### Code:
<pre><code>facerec.train(NAME_OF_PERSON)
</pre></code>

NAME_OF_PERSON = string, i.e.

<pre><code>facerec.train('erlendhelgerud')
</pre></code>

The 'train' function takes 30 samples of the person in the image and saves them to att_faces.

##### Note:
For accuracy, only one person can be present in the image.
If the name already exists in att_faces, the training data will be added to the current lot of images.

#### Use facial recognition
##### Code:
<pre><code>while True:
    facerec.predict_face()
</pre></code>

Currently opens a frame with the webcam and predicts the name(s) of face(s) in the image. Also outputs name of prediction to console.
