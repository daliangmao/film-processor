import runpod
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import base64
import io

print("Loading Google FILM model...")
model = hub.load("https://tfhub.dev/google/film/1")
print("Model loaded successfully.")

def preprocess_image(b64_str):
    if ',' in b64_str:
        b64_str = b64_str.split(',')[1]
    img_data = base64.b64decode(b64_str)
    image = Image.open(io.BytesIO(img_data)).convert("RGB")
    image = np.array(image) / 255.0
    return tf.constant(image, dtype=tf.float32)

def postprocess_image(tensor):
    img_np = (tensor.numpy() * 255).astype(np.uint8)
    img_pil = Image.fromarray(img_np)
    buffered = io.BytesIO()
    img_pil.save(buffered, format="JPEG", quality=95)
    return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')

def handler(event):
    job_input = event.get("input", {})
    
    frame1_b64 = job_input.get("frame1")
    frame2_b64 = job_input.get("frame2")
    
    u1 = preprocess_image(frame1_b64)[tf.newaxis, ...]
    u2 = preprocess_image(frame2_b64)[tf.newaxis, ...]
    
    inference_input = {'x0': u1, 'x1': u2, 'time': tf.constant([0.5], dtype=tf.float32)}
    result = model(inference_input)
    interpolated_frame = result['image'][0]
    
    return {
        "interpolated_frames": [postprocess_image(interpolated_frame)]
    }

runpod.serverless.start({"handler": handler})
