import os
import io
import base64
# pyrefly: ignore [missing-import]
import pytest
from PIL import Image
from app import create_app

@pytest.fixture
def client():
    """Flask test client fixture."""
    app = create_app('test')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def create_sample_base64_image() -> str:
    """Creates a sample 28x28 grayscale image as base64 string."""
    img = Image.new('L', (28, 28), color=255)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

def test_health_endpoint(client):
    """Test /health endpoint returns 200 and healthy status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['model_loaded'] is True

def test_about_endpoint(client):
    """Test /about endpoint returns project architecture info."""
    response = client.get('/about')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'DigitVision AI'
    assert 'architecture' in data

def test_index_page(client):
    """Test home route renders HTML correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'DigitVision AI' in response.data

def test_predict_canvas_success(client):
    """Test canvas prediction endpoint with valid base64 payload."""
    base64_img = create_sample_base64_image()
    response = client.post('/predict-canvas', json={'image': base64_img})
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 'confidence' in data
    assert 0 <= data['prediction'] <= 9


def test_preprocess_image_accepts_pil_image():
    """Ensure preprocess_image supports PIL Image objects directly."""
    from app.preprocessing import preprocess_image

    img = Image.new('L', (28, 28), color=255)
    processed = preprocess_image(img)

    assert processed.shape == (1, 28, 28)
    assert processed.dtype == 'float32'
    assert 0.0 <= processed.min() <= 1.0
    assert 0.0 <= processed.max() <= 1.0

def test_predict_canvas_invalid_payload(client):
    """Test canvas prediction endpoint with invalid payload returns 400."""
    response = client.post('/predict-canvas', json={'invalid': 'data'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_predict_upload_success(client):
    """Test image upload endpoint with valid PNG image file."""
    img = Image.new('L', (28, 28), color=255)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    response = client.post(
        '/predict',
        data={'file': (img_byte_arr, 'test_digit.png')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 'confidence' in data

def test_predict_upload_invalid_extension(client):
    """Test image upload endpoint with disallowed extension returns 400."""
    data = {'file': (io.BytesIO(b"dummy text"), 'test_script.txt')}
    response = client.post('/predict', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_404_not_found(client):
    """Test non-existent route returns 404."""
    response = client.get('/non-existent-route')
    assert response.status_code == 404
