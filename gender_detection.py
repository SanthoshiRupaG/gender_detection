import cv2
import numpy as np

# Paths to model files
FACE_PROTO = "models/deploy.prototxt"
FACE_MODEL = "models/res10_300x300_ssd_iter_140000.caffemodel"
GENDER_PROTO = "models/gender_deploy.prototxt"
GENDER_MODEL = "models/gender_net.caffemodel"

# Load pre-trained models
face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO, GENDER_MODEL)

GENDER_LIST = ['Male', 'Female']

def analyze_video(video_source):
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
        face_net.setInput(blob)
        detections = face_net.forward()

        men_count = 0
        women_count = 0

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype("int")
                face = frame[y1:y2, x1:x2]

                if face.shape[0] > 0 and face.shape[1] > 0:
                    face_blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
                                                      (78.4263377603, 87.7689143744, 114.895847746),
                                                      swapRB=False, crop=False)
                    gender_net.setInput(face_blob)
                    gender_preds = gender_net.forward()
                    gender = GENDER_LIST[gender_preds[0].argmax()]

                    if gender == "Male":
                        men_count += 1
                        color = (255, 0, 0)  # Blue for males
                    else:
                        women_count += 1
                        color = (0, 255, 0)  # Green for females

                    # Draw a rectangle around the face and label it with gender
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, gender, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Overlay the counts on the frame
        cv2.putText(frame, f"Men: {men_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Women: {women_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Encode the frame and send it to the browser
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
