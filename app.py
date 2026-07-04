import os
import cv2
import dlib
import numpy as np
import serial  # Import pyserial library
import time

# 🔌 SERIAL INITIALIZATION: Configured for Native Adafruit Metro ESP32-S3 USB
try:
    esp32 = serial.Serial(
        port='/dev/ttyACM0', 
        baudrate=115200, 
        timeout=1,
        rtscts=True,   # Handle hardware flow-control handshake
        dsrdtr=True    # Manage native USB CDC data carrier lines
    )
    time.sleep(2)  # Allow hardware interface to cleanly initialize
    print("🔌 Successfully connected to Adafruit ESP32-S3 via Serial!")
except Exception as e:
    print(f"⚠️ Warning: Could not open Serial port. Hardware transmission disabled. Error: {e}")
    esp32 = None

print("⏳ Initializing models... Hang tight!")
detector = dlib.get_frontal_face_detector()
recognizer = cv2.face.LBPHFaceRecognizer_create()

KNOWN_FACES_DIR = "known_faces"
images = []
labels = []
names_map = {}

print("📂 Loading known faces from folder...")
current_id = 0

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if gray_img is None:
            continue
            
        faces = detector(gray_img, 1)
        if len(faces) == 0:
            print(f"⚠️ Warning: No face detected in '{filename}'. Make sure it's clear!")
            
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            face_roi = gray_img[max(0, y):min(y+h, gray_img.shape[0]), max(0, x):min(x+w, gray_img.shape[1])]
            if face_roi.size > 0:
                images.append(cv2.resize(face_roi, (200, 200)))
                labels.append(current_id)
                
        # --- FIX: Split by underscore to clean up '_1', '_2', '_3' from names ---
        base_name = os.path.splitext(filename)[0]
        clean_name = base_name.split('_')[0].capitalize()
        
        names_map[current_id] = clean_name
        print(f"Loaded template for: {clean_name} (from {filename})")
        current_id += 1

if len(images) == 0:
    print("❌ Error: Could not train. No faces found in 'known_faces' folder.")
    exit()

print("🧠 Training identification engine...")
recognizer.train(images, np.array(labels))
print("✅ System Ready! Launching Webcam...")

video_capture = cv2.VideoCapture(0)
last_sent_time = 0  # Debounce timer tracking transmission timestamps

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_frame, 1)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        face_roi = gray_frame[max(0, y):min(y+h, frame.shape[0]), max(0, x):min(x+w, frame.shape[1])]
        
        name = "Unknown"
        if face_roi.size > 0:
            face_roi = cv2.resize(face_roi, (200, 200))
            label_id, confidence = recognizer.predict(face_roi)
            
            print(f"Detected face math distance: {confidence:.2f}")
            
            if confidence < 140: 
                name = names_map.get(label_id, "Unknown")
                
                # Transmit data to ESP32 every 2 seconds when verified match drops in
                current_time = time.time()
                if esp32 and name != "Unknown" and (current_time - last_sent_time > 2):
                    esp32.write(f"{name}\n".encode('utf-8'))
                    print(f"🚀 Transmitted to hardware: {name}")
                    last_sent_time = current_time

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y+h - 35), (x+w, y+h), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f"{name}", (x + 6, y+h - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    cv2.imshow('Face Recognition System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if esp32:
    esp32.close()
video_capture.release()
cv2.destroyAllWindows()