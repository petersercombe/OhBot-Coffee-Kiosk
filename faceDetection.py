def faceDetection():
    import cv2
    from ohbot import ohbot

    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print ("Camera detected")
    else:
        print ("Camera not detected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    headX, headY = 4.2, 4
    ohbot.move(ohbot.HEADTURN, headX)
    ohbot.move(ohbot.HEADNOD, headY)
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            if h > 60:
                if x + w/2 > 370:
                    headX -= 0.1
                elif x + w/2 < 320:
                    headX += 0.1
                if y + h/2 > 240:
                    headY -= 0.1
                elif y + h/2 < 200:
                    headY += 0.1
            ohbot.move(ohbot.HEADTURN, headX)
            ohbot.move(ohbot.HEADNOD, headY)

        cv2.imshow('Face Follower', frame)
        ohbot.wait(0.03)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ohbot.close()


if __name__ == "__main__":
    faceDetection()