from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import cv2 as cv
import face_recognition
import os

# Load and encode images from the specified directory
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

path = 'images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encodeListKnown = findEncodings(images)

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            face_locs = face_recognition.face_locations(frame_rgb)
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locs)

            for face_loc, face_encoding in zip(face_locs, face_encodings):
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = classNames[first_match_index]

                top, right, bottom, left = face_loc
                cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv.putText(frame, name, (left, top - 10), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

            # Convert the frame to texture
            buf = cv.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

class MainApp(App):
    def build(self):
        layout = BoxLayout()
        self.camera = KivyCamera()
        layout.add_widget(self.camera)
        return layout

if __name__ == '__main__':
    MainApp().run()
