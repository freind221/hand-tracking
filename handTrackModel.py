import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.pTime = 0
        self.cTime = 0

    def find_hands(self, img):
        imageRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRgb)

        if self.results.multi_hand_landmarks:
            for handLms in  self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
    
    def find_hands_position(self,img, hands=0, draw = False):
        ls = []
        if self.results.multi_hand_landmarks:
            for handLms in  self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c  = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    ls.append([id, cx, cy])
                    if draw:
                        if id==4:
                            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        return ls
    
    def get_fps(self):
        self.cTime = time.time()
        fps = 1/(self.cTime-self.pTime)
        self.pTime = self.cTime
        return fps

    def run(self):
        while True:
            success, img = self.cap.read()

            self.find_hands(img)
            lis = self.find_hands_position(img, draw=True)
            if len(lis)!=0:
                print(lis[4])
            fps = self.get_fps()
            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

            cv2.imshow("Image", img)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    detector = HandDetector()
    detector.run()