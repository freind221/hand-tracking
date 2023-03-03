import cv2
import time
import math
import numpy as num
import handTrackModel as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange =  volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0, None)
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]

detector = htm.HandDetector()

while True:
            success, img = cap.read()

            detector.find_hands(img)
            lis = detector.find_hands_position(img, draw=False)
            if len(lis)!=0:
                x1, y1 = lis[4][1], lis[4][2]
                x2, y2 = lis[8][1], lis[8][2]
                cx, cy = (x1+x2) // 2, (y1+y2)//2
                cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
                cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
                cv2.line(img, (x1,y1),(x2, y2), (255,0,255), 3)
                cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

                length = math.hypot(x2-x1, y2-y1)
                print(length)

                if length<50:
                     cv2.circle(img, (cx,cy), 10, (0,0,0), cv2.FILLED)

                #Hand Range   50 - 300
                #volume Range -69 - 0  
                
                vol = num.interp(length, [50,200], [minVol, maxVol])
                print(vol)
                volume.SetMasterVolumeLevel(vol, None)

            fps = detector.get_fps()
            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

            cv2.imshow("Image", img)

            cv2.waitKey(1)