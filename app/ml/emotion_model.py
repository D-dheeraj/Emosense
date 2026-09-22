import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
from typing import Dict, Tuple, Optional
from app.config import DEVICE, EMOTION_CLASSES, MODEL_WEIGHTS_PATH

class EmoNet(nn.Module):
    """
    Custom 4-Block PyTorch Convolutional Neural Network trained for FER2013
    7-class Facial Emotion Recognition.
    Accelerated on Mac M1 via MPS (Metal Performance Shaders).
    """
    def __init__(self, num_classes: int = 7):
        super(EmoNet, self).__init__()
        
        # Block 1
        self.conv1_1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1_1 = nn.BatchNorm2d(32)
        self.conv1_2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn1_2 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.drop1 = nn.Dropout2d(0.25)
        
        # Block 2
        self.conv2_1 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2_1 = nn.BatchNorm2d(128)
        self.conv2_2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn2_2 = nn.BatchNorm2d(128)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.drop2 = nn.Dropout2d(0.25)

        # Block 3
        self.conv3_1 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3_1 = nn.BatchNorm2d(256)
        self.conv3_2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn3_2 = nn.BatchNorm2d(256)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.drop3 = nn.Dropout2d(0.25)

        # Dense Classifier (Input size for 48x48 image after 3 maxpools (48->24->12->6) is 256 * 6 * 6 = 9216)
        self.fc1 = nn.Linear(256 * 6 * 6, 512)
        self.bn_fc1 = nn.BatchNorm1d(512)
        self.drop_fc1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Block 1
        x = F.relu(self.bn1_1(self.conv1_1(x)))
        x = F.relu(self.bn1_2(self.conv1_2(x)))
        x = self.drop1(self.pool1(x))

        # Block 2
        x = F.relu(self.bn2_1(self.conv2_1(x)))
        x = F.relu(self.bn2_2(self.conv2_2(x)))
        x = self.drop2(self.pool2(x))

        # Block 3
        x = F.relu(self.bn3_1(self.conv3_1(x)))
        x = F.relu(self.bn3_2(self.conv3_2(x)))
        x = self.drop3(self.pool3(x))

        # Flatten & Classify
        x = x.view(x.size(0), -1)
        x = F.relu(self.bn_fc1(self.fc1(x)))
        x = self.drop_fc1(x)
        x = self.fc2(x)
        return x


class FacialEmotionClassifier:
    def __init__(self, model_path: Optional[str] = None):
        self.device = DEVICE
        self.model = EmoNet(num_classes=len(EMOTION_CLASSES))
        self.model.to(self.device)
        self.model.eval()

        weights_path = model_path or MODEL_WEIGHTS_PATH
        if os.path.exists(weights_path):
            try:
                state_dict = torch.load(weights_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                print(f"[EmoNet] Loaded pre-trained weights from {weights_path} onto {self.device}")
            except Exception as e:
                print(f"[EmoNet] Error loading weights ({e}), using initialized model.")
        else:
            # Ensure model directory exists and save initialized weights
            os.makedirs(os.path.dirname(weights_path), exist_ok=True)
            torch.save(self.model.state_dict(), weights_path)
            print(f"[EmoNet] Created base model weights at {weights_path} on {self.device}")

    def preprocess_face(self, face_gray: np.ndarray) -> torch.Tensor:
        """
        Preprocesses a 2D grayscale face array into a 4D PyTorch tensor (1, 1, 48, 48).
        """
        # Resize to 48x48 standard FER2013 size
        img = Image.fromarray(face_gray).resize((48, 48), Image.Resampling.BILINEAR)
        arr = np.array(img, dtype=np.float32) / 255.0  # Normalize [0, 1]
        
        # Standardize (Mean=0.5, Std=0.5)
        arr = (arr - 0.5) / 0.5
        
        tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        return tensor.to(self.device)

    def predict(self, face_gray: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """
        Runs PyTorch CNN inference on cropped grayscale face.
        Returns: (dominant_emotion, confidence, dict_of_all_probabilities)
        """
        tensor = self.preprocess_face(face_gray)
        with torch.no_grad():
            outputs = self.model(tensor)
            probs = F.softmax(outputs, dim=1).cpu().numpy()[0]

        prob_dict = {EMOTION_CLASSES[i]: float(probs[i]) for i in range(len(EMOTION_CLASSES))}
        dominant_idx = int(np.argmax(probs))
        dominant_emotion = EMOTION_CLASSES[dominant_idx]
        confidence = float(probs[dominant_idx])

        return dominant_emotion, confidence, prob_dict


# Singleton Instance
_emotion_classifier: Optional[FacialEmotionClassifier] = None

def get_emotion_classifier() -> FacialEmotionClassifier:
    global _emotion_classifier
    if _emotion_classifier is None:
        _emotion_classifier = FacialEmotionClassifier()
    return _emotion_classifier
