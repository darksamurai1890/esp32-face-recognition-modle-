# Local Edge Face Recognition with Hardware Serial Feedback

A cross-platform computer vision and machine learning pipeline that executes real-time face tracking on a host machine and securely transmits authentication tokens down a low-latency serial data pipe to an attached microcontroller over native USB stacks.

## ⚙️ System Architecture (Ubuntu Setup)
1. **Local Tracking Engine:** Captures frame matrices from a video stream device and extracts facial landmark vectors using `OpenCV` and `dlib`.
2. **Identification Scoring:** Classifies the face using an LBPH Face Recognizer, filtering out frame noise by monitoring mathematical feature distances.
3. **Data Transport:** Transmits the verified identification strings across a native USB CDC serial pipeline (`/dev/ttyACM0`) using structural flow control mapping (`rtscts=True`, `dsrdtr=True`).

## 🚀 Quick Start on Ubuntu Linux

### 1. System Prerequisites
Ensure your system packages and core C++ compilers are up to date:
```bash
sudo apt update
sudo apt install build-essential cmake micro

python3 -m venv face_env
source face_env/bin/activate
pip install opencv-python numpy pyserial dlib

sudo ./face_env/bin/python app.py
---

### 🚀 3. Initialize Git and Push to GitHub

Go to [GitHub.com](https://github.com), log into your account, click the **New** repository button, name it, and leave it completely blank (do **not** check the boxes to initialize with a README or .gitignore, as we just made them locally). 

Once created, copy the repository URL (e.g., `https://github.com/your-username/your-repo-name.git`) and execute these terminal commands inside your project folder:

```bash
# 1. Initialize your local directory as a Git repository
git init

# 2. Stage all your project files (this skips 'face_env' automatically via your .gitignore)
git add .

# 3. Create your initial codebase snapshot commit
git commit -m "Initial commit: Core Ubuntu face recognition with native USB serial architecture"

# 4. Set the default deployment branch name to main
git branch -M main

# 5. Link your local project folder to your remote GitHub repository url
git remote add origin https://github.com/your-username/your-repo-name.git

# 6. Push your files securely to the cloud
git push -u origin main
