# DigitVision AI - Handwritten Digit Recognition Web Application

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**DigitVision AI** is an enterprise-grade, production-ready handwritten digit recognition web application powered by **Flask** and **TensorFlow / Keras**.

> *"Draw it. Upload it. Let AI Recognize It."*

---
---

**Build Status**

- **Local server**: Failed to start on last run (`python app.py`) — exit code 1. Check `logs/app.log` and the console traceback for details.
- **Frontend JS syntax**: `node --check static/js/app.js` returned no parse errors (OK).
- **Note**: Recent experimental edits (feedback/modal features) were reverted in the workspace; if you re-enable them, validate the corresponding HTML IDs and Bootstrap bundle loading order.

## 🌟 Key Features

- 🎨 **Interactive Canvas Studio**: $320 \times 320$ HTML5 canvas with touch & mouse support, anti-aliased drawing brush, live thickness slider, undo stroke history, and drawing download.
- 📁 **Drag & Drop Image Upload**: Supports PNG, JPG, and JPEG files with instant image preview, size validation, and metadata extraction.
- ⚙️ **Automated Preprocessing Pipeline**: Grayscale conversion, auto color inversion (ensuring white digits on black background matching MNIST format), anti-aliasing $28 \times 28$ resizing, and normalization ($x / 255.0$).
- 🧠 **Pre-trained Keras Model Inference**: Singleton model loader configured to load `mnist_model.h5` (.h5/.keras). Loads once on startup for maximum speed.
- 📊 **Rich Prediction Analytics**: Real-time confidence score percentage, radial indicator, animated progress bar, low-confidence warning (<70%), and full 10-class probability breakdown.
- 📜 **Local Storage Prediction History**: Retains the last 10 prediction sessions with thumbnails, timestamps, source tags (Canvas/Upload), and individual delete/clear actions.
- 🌙 **Modern Glassmorphism Design**: Dark/Light mode theme switcher, Bootstrap 5 UI, Poppins typography, AOS scroll animations, and full responsiveness across mobile, tablet, and desktop.

---

## 📁 Project Architecture & Structure

```
digitvision-ai/
│
├── app.py                      # Main entry point for local execution & WSGI
├── config.py                   # Global configuration & environment profiles
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment process manager (Gunicorn)
├── runtime.txt                 # Python runtime version
├── README.md                   # Complete documentation
├── .gitignore                  # Git ignore rules
│
├── model/                      # Model weights directory
│   └── latest_model.h5         # Trained HDF5 Keras model artifact
│
├── app/                        # Application core package
│   ├── __init__.py             # Flask app factory & logging setup
│   ├── routes.py               # Blueprint routes (/predict, /predict-canvas, /health)
│   ├── predictor.py            # Singleton model loader & inference service
│   ├── preprocessing.py        # Dedicated image preprocessing module
│   └── utils.py                # Base64 decoder & secure upload helpers
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Base layout, navbar, footer & CDN references
│   └── index.html              # Main dashboard & interactive studio UI
│
├── static/                     # Static frontend assets
│   ├── css/
│   │   └── style.css           # Modern design system & CSS variables
│   └── js/
│       └── app.js              # Canvas, upload, API & history manager
│
├── uploads/                    # Secure upload storage for audit logs
├── logs/                       # Rotating application log files
└── tests/                      # Automated test suite
    └── test_prediction.py      # Pytest API & route tests
```

---

## 🚀 Quick Start & Local Setup

### Prerequisites
- Python 3.11+
- Git

### 1. Clone & Navigate to Repository
```bash
cd Vision
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite:
```bash
pytest tests/test_prediction.py -v
```

---

## 📡 API Reference

### 1. Upload Prediction
- **Endpoint**: `POST /predict`
- **Content-Type**: `multipart/form-data`
- **Body**: `file` (Image File)
- **Response**:
```json
{
  "prediction": 7,
  "confidence": 99.32,
  "execution_time_ms": 12.45,
  "probabilities": {
    "0": 0.01, "1": 0.02, "2": 0.05, "3": 0.10, "4": 0.00,
    "5": 0.05, "6": 0.00, "7": 99.32, "8": 0.20, "9": 0.25
  }
}
```

### 2. Canvas Base64 Prediction
- **Endpoint**: `POST /predict-canvas`
- **Content-Type**: `application/json`
- **Body**: `{"image": "data:image/png;base64,..."}`
- **Response**: Same as `/predict`

### 3. Health Check
- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy", "model_loaded": true, "timestamp": "2026-08-01T10:00:00Z"}`

---

## ☁️ Deployment Instructions

### Render Deployment
1. Connect GitHub repository to **Render**.
2. Select **Web Service** environment.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`

### Railway Deployment
1. Import repository to **Railway**.
2. Railway auto-detects `Procfile` and `runtime.txt`.
3. Click **Deploy**.

---

## 📄 License
This project is licensed under the MIT License.
