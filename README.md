# GestureRecognizer
Uses OpenCV and MediaPipe to detect hand gestures. This program is able to count the number of fingers that are open on one hand, identify different type of hands signs (Example: peace, rock on, and vulcan salute), and can play rock, paper scissors.

# How to use
- On line 133 change the type of hand gestures you would like to identify by editing detector.gestureRecognizer(landmarklist, type)
- the second parameter type can be "count" to count the number of fingers, "sign" to detect different types of hand signs, and "play" to play rock paper scissors

# What I Learned 
- Utilizing the Mediapipe library to extracting the x and y position of every landmark on the hand and using that information to detect whether a finger is open or close.
- Implementing OpenCV to use the webcam and putting text on the screen.

# Demo
<img src="gifs/sign.gif" height="450"> <img src="gifs/count.gif" height="450">
