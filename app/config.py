import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Database Config
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/emosense.db")

# Google Gemini API Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# PyTorch Device Selection (Apple Silicon MPS / CUDA / CPU)
def get_torch_device():
    try:
        import torch
        if torch.backends.mps.is_available():
            return torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
    except ImportError:
        pass
    return "cpu"

DEVICE = get_torch_device()

# FER2013 Emotion Categories
EMOTION_CLASSES = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Model Paths
MODEL_WEIGHTS_PATH = BASE_DIR / "models_weights" / "fer2013_custom_cnn.pth"
HAAR_CASCADE_PATH = BASE_DIR / "app" / "ml" / "haarcascade_frontalface_default.xml"
