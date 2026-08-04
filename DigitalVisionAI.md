You are a Principal Software Engineer, Senior Machine Learning Engineer, Full Stack Developer, UI/UX Designer, DevOps Engineer, and Software Architect with 15+ years of experience building production AI applications.

Your task is to build a production-ready MNIST Digit Recognition Web Application using Flask.

I already have a trained MNIST model.

DO NOT retrain the model.

Your responsibility is only to load the model and perform inference.

The final application should be clean enough to showcase in interviews and deploy publicly.

PRIMARY OBJECTIVE

Build a beautiful AI web application that allows users to:

✅ Upload an image of a handwritten digit

✅ Draw a handwritten digit on an interactive canvas

✅ Predict the digit using the trained CNN model

✅ Display confidence score

✅ Display prediction history

✅ Clear previous searches

✅ Beautiful animations

✅ Responsive UI

✅ Production folder structure

IMPORTANT

The trained model already exists.

Automatically detect whether the uploaded model is:

.keras
.h5

Load whichever is available.

Never retrain.

Never regenerate weights.

Only inference.

TECHNOLOGY STACK

Backend

Python 3.11+
Flask
TensorFlow/Keras
Pillow
NumPy
OpenCV (if required)
Gunicorn

Frontend

HTML5
CSS3
Vanilla JavaScript
Bootstrap 5

Deployment

Flask
Gunicorn
Render
Railway
Azure App Service
APPLICATION NAME

MNIST AI

Subtitle

Draw it. Upload it. Let AI Recognize It.

APPLICATION FEATURES
1. Premium Landing Page

Create a premium landing page similar to modern AI SaaS websites.

Include:

Hero section
AI illustration
Gradient background
Glassmorphism cards
Floating shapes
Smooth animations
Responsive layout

Hero Heading

Handwritten Digit Recognition using Deep Learning

Subtitle

Upload an image or draw a digit and let AI recognize it instantly.

Buttons

Try Now
Learn More
2. DRAW DIGIT

Build a smooth HTML5 Canvas.

Requirements

Black canvas

White brush

Brush size slider

Touch support

Mouse support

Undo button

Clear button

Predict button

Download drawing button

Canvas size around

320 × 320

Use anti-aliasing.

Make drawing experience smooth.

3. IMAGE UPLOAD

Allow:

PNG

JPG

JPEG

Drag & Drop

Browse File

Preview uploaded image

Replace image

Remove image

Show filename

Show file size

Validate format

Validate size

4. IMAGE PREPROCESSING

Before prediction:

Convert to grayscale

Resize to

28×28

Normalize

pixel / 255

Invert colors automatically if required.

Reshape exactly to model input.

Do preprocessing inside a dedicated utility.

Never duplicate preprocessing logic.

5. PREDICTION CARD

After prediction show

Large predicted digit

Confidence score

Animated progress bar

Confidence circle

Success animation

Display something like

Prediction

8

Confidence

99.32%

If confidence is below

70%

Show warning

AI isn't fully confident. Try drawing more clearly.

6. PREDICTION HISTORY

Store last

10

predictions.

Include

Small thumbnail

Prediction

Confidence

Timestamp

Prediction source

Upload
Canvas

Provide

Clear History

Delete individual history

Use LocalStorage.

7. ABOUT SECTION

Explain

What is MNIST

How CNN works

How preprocessing works

How AI predicts

Use beautiful infographic cards.

UI/UX REQUIREMENTS

The UI should look comparable to premium AI products like:

ChatGPT
Midjourney
Claude
HuggingFace Spaces
Vercel Dashboard

Theme

Modern

Minimal

Professional

Premium

Responsive

Use lots of whitespace.

Rounded corners.

Smooth shadows.

Glassmorphism.

Micro animations.

Hover effects.

COLOR PALETTE

Primary

#2563EB

Secondary

#7C3AED

Accent

#06B6D4

Dark

#0F172A

Background

#F8FAFC

Success

#22C55E

Warning

#F59E0B

Danger

#EF4444
TYPOGRAPHY

Google Font

Poppins

Weights

400

500

600

700

ICONS

Bootstrap Icons

or

Font Awesome

ANIMATIONS

Use

AOS

CSS animations

Fade

Slide

Zoom

Hover lift

Button ripple

Card hover

Loading spinner

Prediction animation

Progress animation

Toast notifications

NAVBAR

Sticky navbar

Logo

MNIST AI

Menu

Home

Predict

History

About

GitHub

Dark Mode Toggle

FOOTER

Include

GitHub

LinkedIn

Email

Copyright

Built with

Flask ❤️ TensorFlow

BACKEND ARCHITECTURE

Follow SOLID principles.

Separate responsibilities.

Never write everything inside app.py.

PRODUCTION FOLDER STRUCTURE
mnist-ai/

│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── Procfile
├── .gitignore
├── runtime.txt
│
├── model/
│     mnist_model.keras
│
├── app/
│
│     __init__.py
│
│     routes.py
│
│     predictor.py
│
│     preprocessing.py
│
│     utils.py
│
│     config.py
│
│
├── templates/
│
│     base.html
│
│     index.html
│
├── static/
│
│     css/
│          style.css
│
│     js/
│          app.js
│
│     images/
│
│     icons/
│
├── uploads/
│
├── logs/
│
│     app.log
│
├── tests/
│
│     test_prediction.py
│
└── instance/
FLASK ROUTES

Create

GET /

Home page

POST /predict

Upload prediction

POST /predict-canvas

Canvas prediction

GET /health

Health check

GET /about

About page

API RESPONSE

Success

{
  "prediction": 7,
  "confidence": 99.28
}

Failure

{
  "error": "Invalid image."
}
SECURITY

Secure filename

Validate extension

Limit upload size

Reject executable files

Handle malformed requests

Handle corrupted images

Prevent crashes

LOGGING

Use Python logging.

Log

Application startup

Model loaded

Prediction requests

Errors

Warnings

Execution time

PERFORMANCE

Load the model only once during application startup.

Never reload the model on every prediction.

Optimize preprocessing.

Use lazy loading where appropriate.

CODE QUALITY

Follow

PEP8

Type hints

Docstrings

Reusable functions

No duplicated code

Meaningful variable names

Meaningful function names

Modular architecture

README

Generate a professional README including

Project overview

Architecture

Screenshots placeholders

Folder structure

Installation

Virtual environment

Running locally

Deployment

API documentation

Future improvements

Troubleshooting

License

DEPLOYMENT

Generate everything required for deployment.

requirements.txt

Procfile

runtime.txt

Gunicorn configuration

Render deployment guide

Railway deployment guide

Azure deployment guide

TESTING

Generate

tests/test_prediction.py

Test

Upload prediction

Canvas prediction

404

Invalid file

Health endpoint

WORKFLOW (VERY IMPORTANT)

Do NOT generate the entire project in one response.

Instead:

Analyze the complete project requirements.
Create a detailed implementation plan.
Explain the architecture.
Create the folder structure.
Wait for approval.
Then generate one file at a time.
For each file:
Explain its responsibility.
Generate complete production-ready code.
Mention where it fits in the project.
Wait for confirmation before generating the next file.
Do not skip any file.
Do not use placeholders or incomplete code.
Ensure every generated file is fully runnable.
FINAL GOAL

The finished application should:

Feel like a polished AI SaaS product.
Follow enterprise-grade software architecture.
Be responsive on desktop, tablet, and mobile.
Be easy to maintain and extend.
Be suitable for a portfolio, GitHub showcase, technical interviews, and deployment to production.
Run locally with python app.py.
Deploy successfully with gunicorn app:app.
Use the existing trained MNIST model for inference without any retraining.

Think through the architecture before writing code, prioritize maintainability, and make engineering decisions that reflect real-world production best practices.