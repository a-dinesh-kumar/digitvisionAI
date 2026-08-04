import importlib
import os
import time
import logging
import numpy as np
from numpy.typing import NDArray
from typing import Any, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class DigitPredictor:
    """
    Singleton Class responsible for loading the trained Keras/TensorFlow model
    and executing digit classification inference.
    """
    _instance: Optional['DigitPredictor'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DigitPredictor, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.model_path = None
            cls._instance.load_model()
        return cls._instance
        
    def load_model(self) -> None:
        """
        Scans model directory and loads the available Keras (.keras or .h5) model.
        Does NOT retrain or regenerate model weights.
        """
        model_dir = Config.MODEL_DIR
        candidate_paths: list[str] = []
        
        # 1. Check preferred model names in model/ directory
        for name in Config.PREFERRED_MODEL_NAMES:
            path = os.path.join(model_dir, name)
            if os.path.isfile(path):
                candidate_paths.append(path)
                
        # 2. Check any .keras or .h5 files in model/ directory
        if os.path.exists(model_dir):
            for file in os.listdir(model_dir):
                if file.endswith(('.keras', '.h5')):
                    path = os.path.join(model_dir, file)
                    if path not in candidate_paths:
                        candidate_paths.append(path)
                        
        # 3. Check root folder as fallback
        for file in os.listdir(Config.BASE_DIR):
            if file.endswith(('.keras', '.h5')):
                path = os.path.join(Config.BASE_DIR, file)
                if path not in candidate_paths:
                    candidate_paths.append(path)
                    
        if not candidate_paths:
            logger.warning("No model file found in model/ or root directory.")
            return

        target_path = candidate_paths[0]
        try:
            logger.info(f"Loading trained MNIST model from: {target_path}")
            keras_models = importlib.import_module('keras.models')
            load_model = getattr(keras_models, 'load_model')
            self.model = load_model(target_path, compile=False)
            self.model_path = target_path
            logger.info("Model loaded successfully into memory.")
        except Exception as e:
            logger.error(f"Failed to load model from {target_path}: {str(e)}")
            self.model = None
            self.model_path = None

    def is_loaded(self) -> bool:
        """Checks if the Keras model is loaded and ready for prediction."""
        return self.model is not None

    def predict(self, preprocessed_img: NDArray[np.float32]) -> Dict[str, Any]:
        """
        Performs model inference on a preprocessed 28x28 grayscale image array.
        
        Args:
            preprocessed_img: Numpy array of shape (1, 28, 28)
            
        Returns:
            Dict containing:
            - prediction (int): Predicted digit (0-9)
            - confidence (float): Confidence score percentage (0-100)
            - probabilities (dict): Per-digit probability mapping
            - execution_time_ms (float): Inference duration in milliseconds
        """
        if not self.is_loaded():
            # Try reloading model in case it was added after app start
            self.load_model()
            if not self.is_loaded():
                raise RuntimeError("Model is not loaded. Please check that a trained .keras or .h5 model exists in model/.")

        start_time = time.time()
        
        # Ensure array dimensions match model expectations
        if len(preprocessed_img.shape) == 2:
            preprocessed_img = np.expand_dims(preprocessed_img, axis=0)
            
        # Run inference
        probs = self.model.predict(preprocessed_img, verbose=0)[0]
        predicted_digit = int(np.argmax(probs))
        confidence_pct = round(float(probs[predicted_digit]) * 100.0, 2)
        
        execution_time_ms = round((time.time() - start_time) * 1000.0, 2)
        
        # Build per-digit probability breakdown dictionary
        digit_probs = {int(i): round(float(p) * 100.0, 2) for i, p in enumerate(probs)}
        
        logger.info(f"Predicted Digit: {predicted_digit} | Confidence: {confidence_pct}% | Time: {execution_time_ms}ms")
        
        return {
            "prediction": predicted_digit,
            "confidence": confidence_pct,
            "probabilities": digit_probs,
            "execution_time_ms": execution_time_ms
        }

def get_predictor() -> DigitPredictor:
    """Returns the singleton DigitPredictor instance."""
    return DigitPredictor()
