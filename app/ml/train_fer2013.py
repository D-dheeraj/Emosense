import os
import sys
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from pathlib import Path

# Add project root directory to sys.path so 'import app' always succeeds
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.config import DEVICE, EMOTION_CLASSES, MODEL_WEIGHTS_PATH
from app.ml.emotion_model import EmoNet

def train_fer2013(dataset_dir: str, epochs: int = 10, batch_size: int = 64, lr: float = 0.001):
    """
    Trains the custom PyTorch EmoNet CNN model on FER2013 dataset using Mac M1 MPS GPU.
    Saves best model weights to models_weights/fer2013_custom_cnn.pth.
    """
    dataset_path = Path(dataset_dir)
    train_dir = dataset_path / "train"
    test_dir = dataset_path / "test"

    if not train_dir.exists() or not test_dir.exists():
        print(f"[Error] Dataset directories not found at {train_dir} and {test_dir}.")
        return

    print("==================================================")
    print("      EmoSense FER2013 PyTorch Model Training     ")
    print("==================================================")
    print(f"Hardware Acceleration Device: {DEVICE} (Mac M1 MPS GPU)")
    print(f"Epochs: {epochs} | Batch Size: {batch_size} | Learning Rate: {lr}\n")

    # 1. Data Augmentation & Normalization Pipeline
    train_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((48, 48)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    test_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((48, 48)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    # 2. PyTorch Datasets & DataLoaders
    train_dataset = datasets.ImageFolder(root=str(train_dir), transform=train_transforms)
    test_dataset = datasets.ImageFolder(root=str(test_dir), transform=test_transforms)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    print(f"[Dataset] Train Samples: {len(train_dataset)} | Test Samples: {len(test_dataset)}")
    print(f"[Classes] {train_dataset.classes}\n")

    # 3. Model, Loss, Optimizer & Scheduler
    model = EmoNet(num_classes=len(EMOTION_CLASSES)).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

    best_acc = 0.0
    start_time = time.time()

    # 4. Training Loop
    for epoch in range(1, epochs + 1):
        epoch_start = time.time()
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for images, labels in train_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += (preds == labels).sum().item()
            total_train += labels.size(0)

        train_loss = running_loss / total_train
        train_acc = (correct_train / total_train) * 100.0

        # Validation Loop
        model.eval()
        test_loss = 0.0
        correct_test = 0
        total_test = 0

        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(DEVICE), labels.to(DEVICE)
                outputs = model(images)
                loss = criterion(outputs, labels)

                test_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                correct_test += (preds == labels).sum().item()
                total_test += labels.size(0)

        val_loss = test_loss / total_test
        val_acc = (correct_test / total_test) * 100.0
        epoch_time = time.time() - epoch_start

        scheduler.step(val_acc)

        print(f"Epoch [{epoch:02d}/{epochs:02d}] ({epoch_time:.1f}s) | Train Loss: {train_loss:.4f} Acc: {train_acc:.2f}% | Val Loss: {val_loss:.4f} Acc: {val_acc:.2f}%")

        # Save Best Model Weights
        if val_acc > best_acc:
            best_acc = val_acc
            os.makedirs(os.path.dirname(MODEL_WEIGHTS_PATH), exist_ok=True)
            torch.save(model.state_dict(), MODEL_WEIGHTS_PATH)
            print(f"  └─► Saved new best model weights ({val_acc:.2f}% Val Acc) -> {MODEL_WEIGHTS_PATH}")

    total_mins = (time.time() - start_time) / 60.0
    print("\n==================================================")
    print(f"Training Complete! Total Time: {total_mins:.2f} mins | Best Accuracy: {best_acc:.2f}%")
    print("==================================================")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent.parent
    dataset_path = base_dir / "dataset"
    train_fer2013(dataset_dir=str(dataset_path), epochs=10, batch_size=64, lr=0.001)
