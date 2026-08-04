import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from app.preprocessing import preprocess_image
from app.predictor import get_predictor
from app.utils import allowed_file, decode_base64_image, save_upload

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Renders main application landing page and UI dashboard."""
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict_upload():
    """
    Endpoint: POST /predict
    Processes uploaded image file (PNG/JPG/JPEG), runs preprocessing, and performs digit prediction.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request.'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading.'}), 400
            
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Only PNG, JPG, and JPEG images are allowed.'}), 400
            
        # Save file securely for audit/logging
        original_name, saved_path = save_upload(file)
        
        # Preprocess uploaded image
        img_array = preprocess_image(saved_path)
        
        # Run inference
        predictor = get_predictor()
        result = predictor.predict(img_array)
        
        logger.info(f"File Upload Prediction: {original_name} -> {result['prediction']} ({result['confidence']}%)")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Prediction error in /predict: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

@main_bp.route('/predict-canvas', methods=['POST'])
def predict_canvas():
    """
    Endpoint: POST /predict-canvas
    Processes base64 encoded canvas image, runs preprocessing, and performs digit prediction.
    """
    try:
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({'error': 'Invalid JSON payload. Key "image" with base64 data required.'}), 400
            
        base64_str = data['image']
        
        # Decode base64 string to PIL Image
        pil_image = decode_base64_image(base64_str)
        
        # Preprocess canvas image
        img_array = preprocess_image(pil_image)
        
        # Run inference
        predictor = get_predictor()
        result = predictor.predict(img_array)
        
        logger.info(f"Canvas Prediction: -> Digit {result['prediction']} ({result['confidence']}%)")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Prediction error in /predict-canvas: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to process canvas image: {str(e)}'}), 500

@main_bp.route('/health', methods=['GET'])
def health():
    """
    Endpoint: GET /health
    Health check endpoint returning application status and model state.
    """
    predictor = get_predictor()
    model_status = predictor.is_loaded()
    
    return jsonify({
        'status': 'healthy' if model_status else 'degraded',
        'model_loaded': model_status,
        'model_path': predictor.model_path if model_status else None,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200 if model_status else 503

@main_bp.route('/about', methods=['GET'])
def about():
    """Endpoint: GET /about - Returns model architecture metadata."""
    return jsonify({
        'name': 'DigitVision AI',
        'subtitle': 'Draw it. Upload it. Let AI Recognize It.',
        'version': '1.0.0',
        'architecture': 'Sequential Feed-Forward Neural Network',
        'layers': [
            'Flatten(input_shape=(28, 28))',
            'Dense(units=256, activation="relu")',
            'Dense(units=128, activation="relu")',
            'Dense(units=10, activation="softmax")'
        ],
        'optimizer': 'adam',
        'loss_function': 'Sparse Categorical Crossentropy',
        'target_classes': 10
    }), 200
