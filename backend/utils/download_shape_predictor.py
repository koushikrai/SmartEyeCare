"""
Script to download Dlib's 68-point facial landmark shape predictor model.
This model is required for blink rate detection.
"""
import os
import urllib.request
import bz2

def download_shape_predictor():
    """Download and extract the shape predictor model"""
    # URLs
    model_url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    
    # Get paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(base_dir)
    models_dir = os.path.join(backend_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    compressed_path = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat.bz2")
    extracted_path = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat")
    
    # Check if already exists
    if os.path.exists(extracted_path):
        print(f"Shape predictor model already exists at: {extracted_path}")
        return extracted_path
    
    print("Downloading shape predictor model...")
    print(f"URL: {model_url}")
    print(f"Destination: {compressed_path}")
    
    try:
        # Download the compressed file
        urllib.request.urlretrieve(model_url, compressed_path)
        print("Download complete!")
        
        # Extract the .bz2 file
        print("Extracting...")
        with bz2.open(compressed_path, 'rb') as f_in:
            with open(extracted_path, 'wb') as f_out:
                f_out.write(f_in.read())
        
        # Remove compressed file
        os.remove(compressed_path)
        print(f"Extraction complete! Model saved to: {extracted_path}")
        return extracted_path
        
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("\nManual download instructions:")
        print(f"1. Download from: {model_url}")
        print(f"2. Extract the .bz2 file")
        print(f"3. Place 'shape_predictor_68_face_landmarks.dat' in: {models_dir}")
        raise

if __name__ == "__main__":
    download_shape_predictor()

