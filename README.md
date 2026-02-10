# 🖐️ AIR CLICK NEXUS

### Hand Gesture Controlled Mouse, Keyboard & Volume System

Control your computer using only **hand gestures** via webcam.
No mouse. No keyboard. Just your hand in the air ✨

Built using **Python + OpenCV + MediaPipe + PyAutoGUI**

---

## 🎥 Features

| Gesture                  | Action               |
| ------------------------ | -------------------- |
| 🤏 Thumb + Index touch   | Mouse Click          |
| ✌️ Index & Middle spread | Volume Up            |
| 🤞 Index & Middle close  | Volume Down          |
| 👍 Thumbs Up             | Screenshot           |
| ✋ Hand High              | Arrow Up             |
| ✋ Hand Low               | Arrow Down           |
| 🤏 + 🤞 Close Together   | ESC key              |
| ☝️ Index finger move     | Mouse Cursor Control |

---

## 🧠 How it Works

The system uses **MediaPipe Hand Tracking** to detect finger landmarks in real time.
Finger distances are calculated using **NumPy** and converted into system actions using **PyAutoGUI**.

Pipeline:

```
Webcam → Hand Detection → Gesture Detection → OS Control
```

---

## 🛠️ Tech Stack

* Python 3.11
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

---

## ⚙️ Requirements

⚠️ MediaPipe does NOT support Python 3.13 yet.
Use **Python 3.11**

Check version:

```bash
py -3.11 --version
```

---

## 📦 Installation

Clone repo:

```bash
git clone https://github.com/yourusername/AirClickNexus.git
cd AirClickNexus
```

Install dependencies:

```bash
py -3.11 -m pip install opencv-python mediapipe pyautogui numpy
```

---

## ▶️ Run the Project

```bash
py -3.11 AIR CLICK NEXUS.py
```

Press **Q** to quit.

---

## 📸 Screenshots Saved Here

Screenshots are automatically saved in project folder:

```
screenshot_YYYYMMDD_HHMMSS.png
```

---

## 🎯 Use Cases

* Touchless computer control
* Accessibility support
* Presentations & demos
* Fun CV/AI project 😄

---

## 🚀 Future Improvements

* Multi-hand gestures
* Gesture customization GUI
* Scroll gesture
* Brightness control
* Gaming mode 🎮

---

## 🙌 Author

**Aditya Raj**

If you like this project ⭐ star the repo!
