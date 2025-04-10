# 🤝 SignSarthi – Indian Sign Language Translator (Software-Only)

**SignSarthi** is a patented AI-powered translator designed to bridge the communication gap between the deaf/mute community and the hearing world. It converts **Indian Sign Language (ISL)** into real-time text and speech, enabling inclusive communication across educational, healthcare, and public domains.

> 🏆 **Patent Granted**: This software solution is officially patented for its novel approach to real-time ISL translation.

---

## 🧩 Problem Statement

The deaf and hard-of-hearing community in India faces significant communication barriers due to the lack of awareness and tools supporting Indian Sign Language (ISL). Existing translation solutions are either inefficient, expensive, or lack real-time capabilities. This hinders access to education, employment, and daily interaction.

---

## 💡 Key Features

- 🔄 **Real-Time ISL Translation**: Instantly convert hand gestures into readable and audible output.
- 🗣 **Text-to-Speech Conversion**: Recognized gestures are transformed into voice for easy understanding.
- 🌐 **Multi-Language Support**: Translations available in multiple Indian languages using APIs.
- 🎓 **ISL Learning Module**: Interactive tool to teach users Indian Sign Language.
- 📞 **On-Call Translation (Prototype Ready)**: Real-time gesture recognition during video or voice calls.

---

## 🧠 Tech Stack

- **Backend**: Python  
- **Frontend**: HTML, CSS, JavaScript  
- **Libraries & Frameworks**: OpenCV, MediaPipe, TensorFlow, Keras, gTTS (Google Text-to-Speech)  
- **Translation APIs**: Used for converting ISL text into multiple Indian languages and speech  

---

## 🔁 Process Flow

1. **Capture Gestures**: Hand gestures are recorded via webcam using OpenCV.
2. **Hand Landmark Detection**: MediaPipe extracts 21 key points from the hand in real-time.
3. **Gesture Classification**: 
   - CNN model classifies static gestures (like alphabets).
   - LSTM model classifies dynamic gestures (like sentences).
4. **Mapping and Output**:
   - Gestures are mapped to corresponding text.
   - Text is displayed and converted into speech using gTTS.
   - Translations are optionally performed into regional languages using translation APIs.

---

## 📦 Installation Guide

### ✅ Prerequisites
- Python 3.8 or above
- A webcam-enabled device

### 🔧 Setup Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/SignSarthi.git
cd SignSarthi
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the translator**
```bash
python app.py
```

**4. Open the Frontend**
Open the `index.html` file from the `frontend/` folder in your browser to interact with the UI built using HTML, CSS, and JavaScript.

---

## 🧠 Software Model Overview

- **MediaPipe**: Detects hand landmarks to generate input data.
- **CNN & LSTM Models**: Classify static and dynamic gestures respectively.
- **Text & Speech Output**: gTTS and REST APIs convert recognized ISL gestures into speech.
- **Multi-Language Translation**: Supports Indian languages for text output via external APIs.
- **Frontend Interface**: Built using HTML, CSS, and JavaScript for real-time interaction with the backend model.

---

## 📜 License & Patent

This project is **patented and protected**. Redistribution or commercial use of the software or its models without prior permission is strictly prohibited.
