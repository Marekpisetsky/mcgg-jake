import json
import os
from typing import List, Tuple

import torch
from PIL import Image
from torchvision import transforms
import torchvision

HEROES = [
    "Layla",
    "Zilong",
    "Tigreal",
    "Franco",
    "Eudora",
    "Saber",
    "Bane",
    "Freya",
    "Karina",
    "Akai",
]

LABELS = {1: "oro", 2: "ronda", 3: "tienda", 4: "sinergia"}

# Add hero labels after the predefined ones
for i, name in enumerate(HEROES, start=5):
    LABELS[i] = name

_transform = transforms.Compose([
    transforms.ToTensor(),
])


class DetectionDataset(torch.utils.data.Dataset):
    """Simple dataset for object detection based on a JSON annotations file."""

    def __init__(self, root: str, annotations: str):
        with open(annotations, "r", encoding="utf-8") as f:
            self.samples = json.load(f)
        self.root = root

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        sample = self.samples[idx]
        image = Image.open(os.path.join(self.root, sample["file"])).convert("RGB")
        boxes = torch.tensor(sample["boxes"], dtype=torch.float32)
        labels = torch.tensor(sample["labels"], dtype=torch.int64)
        target = {"boxes": boxes, "labels": labels}
        return _transform(image), target


def create_model(num_classes: int = len(LABELS) + 1):
    model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(
        weights=None, num_classes=num_classes
    )
    return model


def train_detector(dataset_path: str, annotations: str, out_path: str,
                   epochs: int = 10, lr: float = 1e-3):
    dataset = DetectionDataset(dataset_path, annotations)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True,
                                             collate_fn=lambda x: tuple(zip(*x)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = create_model()
    model.to(device)
    model.train()

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        for images, targets in data_loader:
            images = [img.to(device) for img in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}/{epochs} - Loss: {losses.item():.4f}")
    torch.save(model.state_dict(), out_path)
    print(f"Modelo guardado en {out_path}")


def load_detector(weights: str, device: str | torch.device = "cpu"):
    model = create_model()
    model.load_state_dict(torch.load(weights, map_location=device))
    model.to(device)
    model.eval()
    return model


def detect(model, image: Image.Image, score_thr: float = 0.5) -> List[Tuple[str, List[int], float]]:
    """Run detection on a PIL image and return a list of (label, box, score)."""
    tensor = _transform(image).to(next(model.parameters()).device)
    with torch.no_grad():
        output = model([tensor])[0]
    results = []
    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if score >= score_thr and label.item() in LABELS:
            results.append(
                (LABELS[label.item()], box.cpu().numpy().tolist(), score.item())
            )
    return results


def detect_heroes(model, image: Image.Image, score_thr: float = 0.5) -> tuple[list[str], list[str]]:
    """Detect heroes in shop and bench areas.

    Returns two lists: ``(tienda, banco)``.
    Heroes are sorted from left to right in the shop and appended in order of
    appearance for the bench.
    """
    results = detect(model, image, score_thr)
    shop: list[tuple[float, str]] = []
    bench: list[str] = []
    for label, box, _ in results:
        if label in HEROES:
            x1, y1, x2, y2 = box
            cy = (y1 + y2) / 2
            if cy < image.height * 0.5:
                shop.append((x1, label))
            else:
                bench.append(label)
    shop.sort(key=lambda t: t[0])
    return [l for _, l in shop], bench


def is_shop_visible(model, image: Image.Image, score_thr: float = 0.5) -> bool:
    """Return True if the shop button is detected in the image."""
    results = detect(model, image, score_thr)
    return any(label == "tienda" for label, _, _ in results)
