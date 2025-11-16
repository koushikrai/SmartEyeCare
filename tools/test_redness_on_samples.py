import os
import numpy as np
from PIL import Image

MODEL_PATH = os.path.join('backend','models','redness_model.h5')
DATASET_DIR = os.path.join('backend','dataset','eye_redness_images')

# pick one sample from redness and one from normal
red_dir = os.path.join(DATASET_DIR, 'redness')
normal_dir = os.path.join(DATASET_DIR, 'normal')

red_sample = None
normal_sample = None

for root, dirs, files in os.walk(red_dir):
    for f in files:
        if f.lower().endswith(('.jpg','.jpeg','.png')):
            red_sample = os.path.join(root,f)
            break
    break

for root, dirs, files in os.walk(normal_dir):
    for f in files:
        if f.lower().endswith(('.jpg','.jpeg','.png')):
            normal_sample = os.path.join(root,f)
            break
    break

print('Red sample:', red_sample)
print('Normal sample:', normal_sample)
print('Model path exists:', os.path.exists(MODEL_PATH))

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array
    import tensorflow as tf
    print('TensorFlow version:', tf.__version__)
except Exception as e:
    print('TensorFlow import failed:', e)
    raise

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(MODEL_PATH)

model = load_model(MODEL_PATH)
print('Model loaded')

IMAGE_SIZE = (224,224)

def run_image(path):
    img = Image.open(path).convert('RGB')
    img = img.resize(IMAGE_SIZE)
    arr = img_to_array(img)
    arr = np.expand_dims(arr,0)/255.0
    pred = model.predict(arr)[0]
    idx = int(np.argmax(pred))
    cond = ['normal','redness'][idx]
    conf = float(pred[idx])
    print(f"{os.path.basename(path)} -> {cond} (confidence={conf:.3f}) | raw={pred}")

if red_sample:
    run_image(red_sample)
if normal_sample:
    run_image(normal_sample)
