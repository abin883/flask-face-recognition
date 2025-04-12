from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Load known face encodings
abin_image = face_recognition.load_image_file("Abin/abin.jpg")
abin_face_encoding = face_recognition.face_encodings(abin_image)

jerin_image = face_recognition.load_image_file("Jerin/jerin.jpg")
jerin_face_encoding = face_recognition.face_encodings(jerin_image)

# Initialize known face lists
known_face_encodings = []
known_face_names = []

if abin_face_encoding:
    known_face_encodings.append(abin_face_encoding[0])
    known_face_names.append("Abin")
else:
    print("⚠ Warning: No face found in abin.jpg. Skipping...")

if jerin_face_encoding:
    known_face_encodings.append(jerin_face_encoding[0])
    known_face_names.append("Jerin")
else:
    print("⚠ Warning: No face found in jerin.jpg. Skipping...")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert frame to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Recognize faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            # Draw rectangle and name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        # Yield as HTTP response
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        time.sleep(0.05)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
