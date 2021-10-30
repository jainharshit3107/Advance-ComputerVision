import cv2
import mediapipe as mp
import time

class Handdect():
    def __init__(self, mode=False, maxHands = 2, detectionCon= 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def detectHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    def detectPosition(self, img, handNo=0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList
def main():
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = Handdect()
    while True:
        success, img = cap.read()
        img = detector.detectHands(img)
        # Calling detectPosition function
        lmList = detector.detectPosition(img)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        # for putting frames per second(FPS)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()