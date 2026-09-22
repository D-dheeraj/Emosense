import cv2
import numpy as np
import base64
from typing import Tuple, Optional, Dict, Any

class OpenCVFaceDetector:
    """
    OpenCV Face Detection module.
    Decodes incoming Base64 image frames from webcam stream and extracts cropped face regions.
    Guaranteed fallback to ensure zero runtime crashes.
    """
    def __init__(self):
        self.face_cascade = None
        try:
            if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data'):
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if self.face_cascade.empty():
                    print("[OpenCV] Warning: Loaded Haar cascade is empty.")
                    self.face_cascade = None
        except Exception as e:
            print(f"[OpenCV] Could not load CascadeClassifier ({e}). Center crop fallback active.")
            self.face_cascade = None

    def decode_base64_image(self, base64_str: str) -> Optional[np.ndarray]:
        """
        Decodes base64 string (with or without data:image/jpeg header) to OpenCV BGR image array.
        """
        if not base64_str:
            return None
        try:
            if "," in base64_str:
                base64_str = base64_str.split(",")[1]
            img_bytes = base64.b64decode(base64_str)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            print(f"[OpenCV] Error decoding base64 image: {e}")
            return None

    def detect_and_crop_face(self, bgr_image: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[Dict[str, int]]]:
        """
        Detects primary face in BGR image.
        Returns: (cropped_grayscale_face, bounding_box_dict)
        """
        if bgr_image is None:
            return None, None

        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        
        # Fallback helper function for center crop
        def get_center_crop():
            h, w = gray.shape
            min_dim = min(h, w)
            top = (h - min_dim) // 2
            left = (w - min_dim) // 2
            cropped = gray[top:top+min_dim, left:left+min_dim]
            bbox = {"x": left, "y": top, "w": min_dim, "h": min_dim}
            return cropped, bbox

        if self.face_cascade is None:
            return get_center_crop()

        try:
            gray_eq = cv2.equalizeHist(gray)
            faces = self.face_cascade.detectMultiScale(
                gray_eq,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces) == 0:
                return get_center_crop()

            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            (x, y, w, h) = faces[0]
            
            pad_x = int(w * 0.1)
            pad_y = int(h * 0.1)
            
            y1 = max(0, y - pad_y)
            y2 = min(gray.shape[0], y + h + pad_y)
            x1 = max(0, x - pad_x)
            x2 = min(gray.shape[1], x + w + pad_x)
            
            cropped = gray[y1:y2, x1:x2]
            bbox = {"x": int(x), "y": int(y), "w": int(w), "h": int(h)}
            
            return cropped, bbox
        except Exception as e:
            print(f"[OpenCV] Exception during face detection ({e}), returning center crop.")
            return get_center_crop()


_face_detector: Optional[OpenCVFaceDetector] = None

def get_face_detector() -> OpenCVFaceDetector:
    global _face_detector
    if _face_detector is None:
        _face_detector = OpenCVFaceDetector()
    return _face_detector
