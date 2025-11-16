import cv2
import numpy as np
import os
from scipy.spatial import distance as dist

try:
    # Import face_mesh directly to avoid TensorFlow dependency issues
    from mediapipe.solutions import face_mesh
    from mediapipe.solutions.drawing_utils import DrawingSpec
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: mediapipe is not installed. Blink detection will not work.")
    print("Install with: pip install mediapipe")

# MediaPipe Face Mesh eye landmark indices (468-point model)
# For EAR calculation, we need 6 points per eye in this order:
# [outer_corner, inner_corner, top_1, top_2, bottom_1, bottom_2]
# Left eye: outer(33), inner(133), top(159), top(158), bottom(145), bottom(153)
# Right eye: outer(362), inner(263), top(386), top(387), bottom(374), bottom(380)
LEFT_EYE_INDICES = [33, 133, 159, 158, 145, 153]
RIGHT_EYE_INDICES = [362, 263, 386, 387, 374, 380]

# Eye Aspect Ratio threshold
EAR_THRESHOLD = 0.25
# Consecutive frames below threshold to count as blink
EAR_CONSEC_FRAMES = 2

def eye_aspect_ratio(eye_points):
    """
    Calculate Eye Aspect Ratio (EAR) from 6 eye landmark points.
    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    """
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    
    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye_points[0], eye_points[3])
    
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

class BlinkRateDetector:
    def __init__(self):
        """
        Initialize the blink rate detector using MediaPipe Face Mesh.
        """
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError(
                "mediapipe is not installed. Please install it to use blink detection.\n"
                "Install with: pip install mediapipe"
            )
        
        # Initialize MediaPipe Face Mesh
        self.face_mesh = face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detect_blinks_in_video(self, video_path):
        """
        Detect blinks in a video file and calculate blink rate.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            dict with keys:
                - blink_count: Total number of blinks detected
                - video_duration_seconds: Duration of video in seconds
                - blink_rate: Blinks per minute
                - status: "low", "normal", or "high"
                - frames_processed: Number of frames analyzed
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}. The file may be corrupted or in an unsupported format.")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = frame_count / fps if fps > 0 else 0
        
        # Initialize counters
        blink_counter = 0
        frames_processed = 0
        consecutive_frames = 0
        
        # Process each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe Face Mesh
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                # Use the first detected face
                face_landmarks = results.multi_face_landmarks[0]
                
                # Get image dimensions
                h, w = frame.shape[:2]
                
                # Extract eye landmark points
                left_eye_points = []
                right_eye_points = []
                
                for idx in LEFT_EYE_INDICES:
                    landmark = face_landmarks.landmark[idx]
                    left_eye_points.append([landmark.x * w, landmark.y * h])
                
                for idx in RIGHT_EYE_INDICES:
                    landmark = face_landmarks.landmark[idx]
                    right_eye_points.append([landmark.x * w, landmark.y * h])
                
                # Convert to numpy arrays
                left_eye = np.array(left_eye_points)
                right_eye = np.array(right_eye_points)
                
                # Calculate EAR for both eyes
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)
                
                # Average EAR for both eyes
                ear = (left_ear + right_ear) / 2.0
                
                # Check if eyes are closed (EAR below threshold)
                if ear < EAR_THRESHOLD:
                    consecutive_frames += 1
                else:
                    # If eyes were closed for enough consecutive frames, count as blink
                    if consecutive_frames >= EAR_CONSEC_FRAMES:
                        blink_counter += 1
                    consecutive_frames = 0
                
                frames_processed += 1
        
        cap.release()
        
        # Calculate blink rate (blinks per minute)
        if video_duration > 0:
            blink_rate = (blink_counter / video_duration) * 60
        else:
            blink_rate = 0
        
        # Determine status
        if blink_rate < 12:
            status = "low"
        elif blink_rate > 30:
            status = "high"
        else:
            status = "normal"
        
        return {
            "blink_count": blink_counter,
            "video_duration_seconds": round(video_duration, 2),
            "blink_rate": round(blink_rate, 2),
            "status": status,
            "frames_processed": frames_processed
        }

def detect_blink_rate(video_path):
    """
    Convenience function to detect blink rate in a video.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        dict with blink detection results
    """
    detector = BlinkRateDetector()
    return detector.detect_blinks_in_video(video_path)
