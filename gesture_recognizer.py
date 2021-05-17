import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # formality you have to do to start using this module.
        self.mpHands = mp.solutions.hands
        # first property is static image mode - when set to false it will detect when detection confidence is low and track when there is good tracking confidence.
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        # formality to access the drawing utilities (dots and connections)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):
        # the media pipe object needs the rbg color space
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # takes the img that we passes in and scans it to finds the hands
        self.results = self.hands.process(imgRGB)
        # if landmarks are being detected
        if self.results.multi_hand_landmarks:
            # then draw the landmarks that it finds with dots and connections
            for handLandmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img):
        landmarkList = []
        # if landmarks are being detected
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            for id, lm, in enumerate(myHand.landmark):
                # gives us the width and height of our image
                h, w, c = img.shape
                # we need Width and height because our current x and y values are in decimal places and we
                # want to convert them into pixels.
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkList.append([id, cx, cy])
        return landmarkList

    def gestureRecognizer(self, landmarkList, type):
        thumbState = ""
        indexState = ""
        middleState = ""
        ringState = ""
        pinkyState = ""
        handGesture = ""

        if len(landmarkList) != 0:
            if landmarkList[2][1] > landmarkList[3][1] > landmarkList[4][1]:
                thumbState = "CLOSE"
            elif landmarkList[2][1] < landmarkList[3][1] < landmarkList[4][1]:
                thumbState = "OPEN"

            if landmarkList[6][2] > landmarkList[7][2] > landmarkList[8][2]:
                indexState = "OPEN"
            elif landmarkList[6][2] < landmarkList[7][2] < landmarkList[8][2]:
                indexState = "CLOSE"

            if landmarkList[10][2] > landmarkList[11][2] > landmarkList[12][2]:
                middleState = "OPEN"
            elif landmarkList[10][2] < landmarkList[11][2] < landmarkList[12][2]:
                middleState = "CLOSE"

            if landmarkList[14][2] > landmarkList[15][2] > landmarkList[16][2]:
                ringState = "OPEN"
            elif landmarkList[14][2] < landmarkList[15][2] < landmarkList[16][2]:
                ringState = "CLOSE"

            if landmarkList[18][2] > landmarkList[19][2] > landmarkList[20][2]:
                pinkyState = "OPEN"
            elif landmarkList[18][2] < landmarkList[19][2] < landmarkList[20][2]:
                pinkyState = "CLOSE"

        if type == "count":
            fingers = [thumbState, indexState, middleState, ringState, pinkyState]
            openCount = 0
            for finger in fingers:
                if finger == "OPEN":
                    openCount += 1
            if openCount == 1:
                handGesture = "ONE"
            elif openCount == 2:
                handGesture = "TWO"
            elif openCount == 3:
                handGesture = "THREE"
            elif openCount == 4:
                handGesture = "FOUR"
            elif openCount == 5:
                handGesture = "FIVE"
        elif type == "sign":
            if thumbState == "CLOSE" and indexState == "CLOSE" and middleState == "OPEN" and ringState == "OPEN" and pinkyState == "OPEN":
                handGesture = "OKAY"
            elif thumbState == "OPEN" and indexState == "OPEN" and middleState == "CLOSE" and ringState == "CLOSE" and pinkyState == "OPEN":
                handGesture = "SPIDER MAN"
            elif thumbState == "CLOSE" and indexState == "OPEN" and middleState == "CLOSE" and ringState == "CLOSE" and pinkyState == "OPEN":
                handGesture = "ROCK ON"
            elif thumbState == "CLOSE" and indexState == "OPEN" and middleState == "OPEN" and ringState == "CLOSE" and pinkyState == "CLOSE":
                handGesture = "PEACE"
            elif thumbState == "CLOSE" and indexState == "OPEN" and middleState == "CLOSE" and ringState == "CLOSE" and pinkyState == "CLOSE":
                handGesture = "NUMBER ONE"
            elif thumbState == "OPEN" and indexState == "CLOSE" and middleState == "CLOSE" and ringState == "CLOSE" and pinkyState == "OPEN":
                handGesture = "HANG LOOSE"
            elif thumbState == "OPEN" and indexState == "OPEN" and middleState == "OPEN" and ringState == "OPEN" and pinkyState == "OPEN" and abs(landmarkList[12][1] - landmarkList[16][1]) >= 85:
                handGesture = "VULCAN SALUTE"
            else:
                handGesture = ""
        elif type == "play":
            if thumbState == "CLOSE" and indexState == "CLOSE" and middleState == "CLOSE" and ringState == "CLOSE" and pinkyState == "CLOSE": # ROCK
                handGesture = "COMPUTER CHOOSES PAPER"
            elif thumbState == "CLOSE" and indexState == "OPEN" and middleState == "OPEN" and ringState == "CLOSE" and pinkyState == "CLOSE": # SCISSORS
                handGesture = "COMPUTER CHOOSES ROCK"
            elif thumbState == "OPEN" and indexState == "OPEN" and middleState == "OPEN" and ringState == "OPEN" and pinkyState == "OPEN": # PAPER
                handGesture = "COMPUTER CHOOSES SCISSORS"

        return handGesture

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landmarkList = detector.findPosition(img)

        if len(landmarkList) != 0:
            cv2.putText(img, detector.gestureRecognizer(landmarkList, "play"), (landmarkList[0][1]-50, landmarkList[0][2]-320), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
