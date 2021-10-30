import cv2
import time
import numpy as np
import HandModulee as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################################
# You can set according to your convenience
wCam, hCam = 640, 480
####################################
# 0 for default camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = hm.Handdect(detectionCon=0.7)

# https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0



while True:
    success, img = cap.read()
    img = detector.detectHands(img)
    lmList = detector.detectPosition(img, draw=False)
    if len(lmList) != 0:
        # 4 - Thumb_tip, 8 - Index-finger_tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # Centre of line between 4 & 8
        cx, cy = (x1+x2)//2, (y1+y2) // 2

        # Circle on Thumb_tip
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        # Circle on Index-finger_tip
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # a line between 4 & 8
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)
        # Circle between 4 & 8
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # calculate the square root of the sum of squares of numbers
        length = math.hypot(x2-x1, y2-y1)
        # HandRange 20-240 (can vary with you)
        # Volume Range = -65 - 0

        vol = np.interp(length, [21, 235], [minVol, maxVol])
        volBar = np.interp(length, [21, 235], [400, 150])
        volPer = np.interp(length, [21, 235], [0, 100])
        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<20:
            # When volumes comes to zero a green circle is popped
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Makes a volume rectangle box on screen
    cv2.rectangle(img, (50,150), (85, 400), (255,0,0), 3)
    # Fills the box according to percent volume
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    # Puts the volume percent number on above the box
    cv2.putText(img, f"{int(volPer)}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX,1, (255,0,0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)





