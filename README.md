# Local Edge Face Recognition with Hardware Serial Feedback



An optimized, cross-platform computer vision and machine learning pipeline that executes real-time face tracking on a host machine and transmits authenticated token strings down a low-latency serial data pipe to an attached microcontroller over native USB stacks.

---

## ⚙️ System Architecture

The project splits intensive computer vision calculations onto host hardware while using microcontrollers strictly for edge actuation, bypassing slow networking layers.

+------------------+      Frame Capture      +-------------------------+
|                  | ----------------------> |                         |
|   Video Stream   |                         |  Local Machine Learning |
|  (Webcam / Feed) | <---------------------- |      Engine (Host)      |
|                  |    Landmark Vector      |                         |
+------------------+                         +-------------------------+
|
| Identified Token
| (e.g., "Rajith\n")
v
+------------------+       CDC Pipeline      +-------------------------+
|                  | <---------------------- |                         |
|   Target Edge    |     /dev/ttyACM0        |   Native USB Serial     |
|  Microcontroller |     (rtscts/dsrdtr)     |      Data Transport     |
|                  |                         |                         |
+------------------+                         +-------------------------+

### 🧠 Core Component Engineering
1. **Local Tracking Engine:** Captures frame matrices dynamically from the active video interface and extracts 68-point facial landmark vectors using `OpenCV` and spatial `dlib` processing models.
2. **Identification Scoring:** Processes face signatures using an LBPH (Local Binary Patterns Histograms) classification routine, suppressing background environmental noise by parsing mathematical threshold feature distances.
3. **Hardware Data Transport:** Channels verified text tokens across a native USB CDC serial pipeline (`/dev/ttyACM0` on Linux or `COMx` on Windows) at `115200` baud. It utilizes strict hardware flow control configuration parameters (`rtscts=True`, `dsrdtr=True`) to prevent buffer overflow on the microchip.

---

## 🚀 Quick Start (Ubuntu Linux Setup)

Follow these terminal setup instructions to deploy the tracking pipeline on an Ubuntu-based host system.

### 1. System Prerequisites
Update your core system packages and install the essential C++ compiler engines required to build the low-level vision tracking wrappers from source:
```bash
sudo apt update
sudo apt install build-essential cmake micro -y

# Move into the project root directory
cd ~/face_recognition_project

# Instantiate and activate the isolated runtime space
python3 -m venv face_env
source face_env/bin/activate

# Install high-performance matrix and vision frameworks
pip install opencv-python numpy pyserial dlib
known_faces/
├── profile_name_1.jpg
└── profile_name_2.png

sudo ./face_env/bin/python app.py
⚡ Initializing Hardware Loopback Test on /dev/ttyACM0...
🚀 Sending text out via TX line: 'Hello ESP32-S3 Hardware'
✅ SUCCESS! Received back on RX line: 'ESP32_CONNECTED'
🎉 Your USB data connection is 100% working perfectly!

├── .gitignore               <-- Filters out local heavy virtual environment paths
├── README.md                <-- Project documentation manual
├── app.py                   <-- Core Python face tracking engine
├── ead_esp32.py             <-- Serial loopback diagnostic verification tool
└── known_faces/             <-- Target reference database directory

