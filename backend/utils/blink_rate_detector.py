import cv2
import numpy as np
import os
from scipy.spatial import distance as dist

try:
    # Import face_mesh - correct path is mediapipe.python.solutions
    from mediapipe.python.solutions import face_mesh
    from mediapipe.python.solutions.drawing_utils import DrawingSpec
    MEDIAPIPE_AVAILABLE = True
    MEDIAPIPE_ERROR = None
except ImportError as e:
    # Try alternative import path (older versions)
    try:
        from mediapipe.solutions import face_mesh
        from mediapipe.solutions.drawing_utils import DrawingSpec
        MEDIAPIPE_AVAILABLE = True
        MEDIAPIPE_ERROR = None
    except ImportError:
        MEDIAPIPE_AVAILABLE = False
        MEDIAPIPE_ERROR = str(e)
        print(f"Warning: mediapipe import failed: {e}")
        print("This might be due to:")
        print("1. MediaPipe not installed in the current Python environment")
        print("2. Using wrong Python interpreter (should use Python 3.11 venv)")
        print("3. Protobuf version conflict")
        print("Install with: pip install mediapipe")
except Exception as e:
    MEDIAPIPE_AVAILABLE = False
    MEDIAPIPE_ERROR = str(e)
    print(f"Warning: mediapipe import error: {e}")
    print("This might be a dependency conflict (e.g., protobuf version)")

# MediaPipe Face Mesh eye landmark indices (468-point model)
# For EAR calculation, we need 6 points per eye in this order:
# [outer_corner, inner_corner, top_1, top_2, bottom_1, bottom_2]
# Left eye: outer(33), inner(133), top(159), top(158), bottom(145), bottom(153)
# Right eye: outer(362), inner(263), top(386), top(387), bottom(374), bottom(380)
LEFT_EYE_INDICES = [33, 133, 159, 158, 145, 153]
RIGHT_EYE_INDICES = [362, 263, 386, 387, 374, 380]

# Eye Aspect Ratio threshold
import collections
import os

# Default thresholds (can be overridden by environment variables)
EAR_THRESHOLD = float(os.getenv("EAR_THRESHOLD", "0.25"))
# Consecutive frames below threshold to count as blink
EAR_CONSEC_FRAMES = int(os.getenv("EAR_CONSEC_FRAMES", "2"))
# Moving average window size for EAR smoothing to reduce noise
EAR_SMOOTHING_WINDOW = int(os.getenv("EAR_SMOOTHING_WINDOW", "3"))
# Haar-based fallback parameters
HAAR_CLOSURE_FACTOR = float(os.getenv("HAAR_CLOSURE_FACTOR", "0.55"))
HAAR_BASELINE_ALPHA = float(os.getenv("HAAR_BASELINE_ALPHA", "0.08"))
HAAR_CONSEC_FRAMES = int(os.getenv("HAAR_CONSEC_FRAMES", "2"))

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
        # If MediaPipe is not available, fall back to OpenCV Haar cascades
        if not MEDIAPIPE_AVAILABLE:
            print(f"Warning: MediaPipe not available: {MEDIAPIPE_ERROR}")
            print("Falling back to OpenCV Haar cascade eye detection. This is less accurate but avoids dependency conflicts.")
            # Initialize Haar cascade for eyes
            haar_path = cv2.data.haarcascades
            self.eye_cascade = cv2.CascadeClassifier(os.path.join(haar_path, "haarcascade_eye.xml"))
            self.use_haar = True
        else:
            # Initialize MediaPipe Face Mesh
            self.face_mesh = face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.use_haar = False

        # For smoothing EAR values across frames
        self.ear_deque = collections.deque(maxlen=EAR_SMOOTHING_WINDOW)
        # Haar fallback baseline for edge-density (None until initialized)
        self.haar_baseline = None
    
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
            
            if not self.use_haar:
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
                    raw_ear = (left_ear + right_ear) / 2.0
                else:
                    # No face detected in this frame
                    frames_processed += 1
                    continue
            else:
                # Haar-cascade fallback: detect eyes using OpenCV cascades
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                eyes = self.eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                if len(eyes) == 0:
                    frames_processed += 1
                    continue

                # Sort detections by area (largest first), pick up to two
                eyes_sorted = sorted(eyes, key=lambda e: e[2]*e[3], reverse=True)[:2]

                edge_densities = []
                for (ex, ey, ew, eh) in eyes_sorted:
                    # Extract eye ROI with a small padding
                    pad_x = max(int(0.15 * ew), 2)
                    pad_y = max(int(0.2 * eh), 2)
                    x1 = max(ex - pad_x, 0)
                    y1 = max(ey - pad_y, 0)
                    x2 = min(ex + ew + pad_x, frame.shape[1])
                    y2 = min(ey + eh + pad_y, frame.shape[0])

                    roi = gray[y1:y2, x1:x2]
                    if roi.size == 0:
                        continue

                    # Compute Canny edges and edge density
                    edges = cv2.Canny(roi, 50, 150)
                    edge_count = np.count_nonzero(edges)
                    area = roi.shape[0] * roi.shape[1]
                    density = float(edge_count) / float(area) if area > 0 else 0.0
                    edge_densities.append(density)

                if len(edge_densities) == 0:
                    frames_processed += 1
                    continue

                # Average edge density across detected eyes
                density = float(np.mean(edge_densities))

                # Initialize or update baseline when eyes appear open
                if self.haar_baseline is None:
                    self.haar_baseline = density
                else:
                    # exponential moving average baseline
                    self.haar_baseline = (HAAR_BASELINE_ALPHA * density) + ((1 - HAAR_BASELINE_ALPHA) * self.haar_baseline)

                # Map density to a pseudo-'ear' value in [0,1] by normalizing to baseline
                # When closed, density will drop significantly below baseline
                if self.haar_baseline > 0:
                    raw_ear = density / self.haar_baseline
                else:
                    raw_ear = density

                # Shared processing: smooth EAR, debug log, and count blinks
                # Smooth EAR using moving average to reduce jitter
                self.ear_deque.append(raw_ear)
                ear = float(np.mean(self.ear_deque))

                # Debug logging: print occasional EAR values to help troubleshoot
                if frames_processed % 30 == 0:
                    print(f"Frame {frames_processed}: raw_ear={raw_ear:.3f}, smoothed_ear={ear:.3f}")

                # Select thresholds depending on detection method
                active_threshold = EAR_THRESHOLD if not self.use_haar else HAAR_CLOSURE_FACTOR
                active_consec = EAR_CONSEC_FRAMES if not self.use_haar else HAAR_CONSEC_FRAMES

                # Check if eyes are closed (EAR below threshold)
                if ear < active_threshold:
                    consecutive_frames += 1
                else:
                    # If eyes were closed for enough consecutive frames, count as blink
                    if consecutive_frames >= active_consec:
                        blink_counter += 1
                        print(f"Blink detected at frame {frames_processed}: ear={ear:.3f}, consecutive={consecutive_frames}")
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
