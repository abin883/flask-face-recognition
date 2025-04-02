# Flask Face Recognition Project

## Overview
This is a Flask-based face recognition web application that uses OpenCV and the `face_recognition` library to detect and recognize faces from a webcam stream.

## Features
- Real-time face detection using OpenCV
- Face encoding and recognition with `face_recognition`
- Web-based interface with live streaming
- Flask backend for processing frames

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/flask-face-recognition.git
cd flask-face-recognition
```

### 2. Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
### 1. Run the Flask App
```sh
python app.py
```
The app will start running on:
```
http://127.0.0.1:5000/
```

### 2. Access the Web Interface
Open your browser and go to `http://127.0.0.1:5000/` to view the live webcam stream.

## Troubleshooting
- **No faces detected?**
  - Ensure your webcam is working and positioned correctly.
  - Increase brightness or change lighting conditions.
  - Adjust `face_recognition.face_encodings()` parameters in `app.py`.

- **Camera index out of range error?**
  - Change the camera index in `cv2.VideoCapture(0)` (try `1` or `2` instead of `0`).
  
- **ModuleNotFoundError?**
  - Ensure dependencies are installed correctly using `pip install -r requirements.txt`.

## Contributing
Feel free to fork this repo and submit pull requests!

## License
This project is licensed under the MIT License.

---
Made with ❤️ using Flask, OpenCV, and face_recognition.

