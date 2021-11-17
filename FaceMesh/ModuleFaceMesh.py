import cv2
import mediapipe as mp
import time

class FaceMesh():

    def __init__(self, staticMode = False, maxFaces = 2,
                 landmarks=False,minDetectC = 0.6, minTrackCo = 0.6):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.landmarks = landmarks
        self.minDetectC = minDetectC
        self.minTrackCo = minTrackCo
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.drawSpec = self.mpDraw.DrawingSpec(color = (0, 0, 0),thickness=1, circle_radius=1)
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, self.landmarks,
                                                 self.minDetectC, self.minTrackCo)

    def findFace(self, image, draw = True):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)
        faces = []
        if results.multi_face_landmarks:
            for faceLMS in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, faceLMS, self.mpFaceMesh.FACEMESH_FACE_OVAL,
                                          self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLMS.landmark):
                    # ih, iw, ic - image height, width, channel
                    ih, iw, ic = image.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    face.append([x, y])
                faces.append(face)
        return image, faces

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = FaceMesh()
    pT = 0
    while 1:

        success, image = cap.read()
        image, faces = detector.findFace(image)
        if len(faces) != 0:
            print(f"No. of Faces Detected - {len(faces)}")
        cT = time.time()
        fps = 1 / (cT - pT)
        pT = cT
        cv2.putText(image, f"FPS {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", image)
        cv2.waitKey(1)
