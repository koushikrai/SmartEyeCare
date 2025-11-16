import os
import numpy as np

model_path = os.path.join('backend','models','redness_model.h5')
print('Model path:', model_path, 'exists:', os.path.exists(model_path))

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array
    import tensorflow as tf
    print('TensorFlow version:', tf.__version__)
except Exception as e:
    print('TensorFlow/Keras import failed:', e)
    raise

try:
    model = load_model(model_path)
    print('Model loaded')
    try:
        model.summary()
    except Exception as e:
        print('Could not print model.summary():', e)
    # Try to get input shape
    try:
        inp = model.input_shape
        print('Input shape:', inp)
        if inp and len(inp) >= 4:
            h, w, c = inp[1], inp[2], inp[3]
        else:
            h, w, c = 224, 224, 3
    except Exception as e:
        print('Error getting input shape, defaulting to 224x224x3:', e)
        h, w, c = 224, 224, 3

    # create dummy image with plausible values (scaled 0-1)
    x = np.random.rand(1, h, w, c).astype(np.float32)
    preds = model.predict(x)
    print('Predictions shape:', np.shape(preds))
    print('Predictions sample:', preds[0])
except Exception as e:
    print('Error loading/predicting with model:', e)
    raise
