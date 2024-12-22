#Import library
import cv2
import time

#Import module
import script_gui

faceOn = False
faceDetectedStart = 0
delay = 5
faceDetected = False
alreadyRunning = False

def runFaceDetection():
    global alreadyRunning
    global faceDetected
    global faceOn
    global delay

    faceDetectedStart = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Kamera tidak dapat dibuka.")

    while faceOn and script_gui.windowOpen:
        ret, frame = cap.read()

        if not ret:
            print("Gagal menangkap gambar. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Check apakah terdapat wajah yang terdeteksi
        if not faceDetected:
            if len(faces) > 0:
                faceDetected = True
                faceDetectedStart = time.time()
            else:
                faceDetected = False
        else:
            if len(faces) > 0:
                faceDetectedStart = time.time()
            if (time.time() - faceDetectedStart) > delay:
                faceDetected = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def startCam():
    global alreadyRunning
    global faceOn

    while script_gui.windowOpen:
        time.sleep(1/script_gui.fps)
        if faceOn and not alreadyRunning:
            runFaceDetection()
