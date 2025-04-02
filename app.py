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

# Process every alternate frame
process_this_frame = True

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        print(f"Detected Faces in Flask App: {face_locations}")  # Debugging print

        if not face_locations:
            print("⚠ No faces detected. Skipping encoding.")
            continue  # Skip frame if no face is detected

        # Encode the face
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Draw rectangle around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Convert frame to JPEG format
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        # Yield the frame as an HTTP response
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)