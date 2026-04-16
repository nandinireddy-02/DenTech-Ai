from __future__ import annotations

import argparse
import os
from pathlib import Path

import joblib
import numpy as np
from PIL import Image, ImageOps
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


DEFAULT_DATASET_ROOT = r"C:\Users\bapat\OneDrive\Desktop\datasets iomp"
MODELS_DIR = Path(__file__).resolve().parent / 'models'
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}


def list_images(dataset_dir: Path) -> list[Path]:
    return [
        p
        for p in dataset_dir.rglob('*')
        if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS
    ]


def image_to_vector(image_path: Path, image_size: int = 96) -> np.ndarray:
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert('L').resize((image_size, image_size))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr.reshape(-1)


def train_one_class_model(
    image_paths: list[Path],
    model_output_path: Path,
    image_size: int = 96,
    contamination: float = 0.1,
) -> dict:
    x = np.stack([image_to_vector(p, image_size=image_size) for p in image_paths], axis=0)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    n_samples, n_features = x_scaled.shape
    pca_components = int(min(128, n_samples - 1, n_features))
    pca_components = max(2, pca_components)

    pca = PCA(n_components=pca_components, random_state=42)
    x_reduced = pca.fit_transform(x_scaled)

    forest = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=300,
        n_jobs=-1,
    )
    forest.fit(x_reduced)

    scores = forest.decision_function(x_reduced)
    threshold = float(np.percentile(scores, 15))

    model_bundle = {
        'image_size': image_size,
        'scaler': scaler,
        'pca': pca,
        'isolation_forest': forest,
        'threshold': threshold,
        'train_size': len(image_paths),
    }

    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_bundle, model_output_path)

    return {
        'train_size': len(image_paths),
        'pca_components': pca_components,
        'threshold': threshold,
        'output': str(model_output_path),
    }


def resolve_dataset_paths(dataset_root: Path) -> tuple[Path, Path]:
    hypodontia_dir = dataset_root / 'hypodontia'

    discoloration_dir = dataset_root / 'tooth discoloration original dataset'
    nested_discoloration_dir = discoloration_dir / 'tooth discoloration original dataset'
    if nested_discoloration_dir.exists():
        discoloration_dir = nested_discoloration_dir

    return hypodontia_dir, discoloration_dir


def main() -> None:
    parser = argparse.ArgumentParser(description='Train DenTech AI one-class models.')
    parser.add_argument(
        '--dataset-root',
        default=DEFAULT_DATASET_ROOT,
        help='Root folder containing hypodontia and discoloration datasets',
    )
    parser.add_argument(
        '--image-size',
        type=int,
        default=96,
        help='Square size to resize images before feature extraction',
    )
    parser.add_argument(
        '--contamination',
        type=float,
        default=0.1,
        help='Expected outlier ratio for IsolationForest',
    )
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root)
    hypodontia_dir, discoloration_dir = resolve_dataset_paths(dataset_root)

    if not hypodontia_dir.exists():
        raise FileNotFoundError(f'Hypodontia dataset not found: {hypodontia_dir}')
    if not discoloration_dir.exists():
        raise FileNotFoundError(f'Discoloration dataset not found: {discoloration_dir}')

    hypodontia_images = list_images(hypodontia_dir)
    discoloration_images = list_images(discoloration_dir)

    if len(hypodontia_images) < 20:
        raise RuntimeError('Need at least 20 hypodontia images for training.')
    if len(discoloration_images) < 20:
        raise RuntimeError('Need at least 20 discoloration images for training.')

    hypodontia_model_path = MODELS_DIR / 'hypodontia_model.joblib'
    discoloration_model_path = MODELS_DIR / 'discoloration_model.joblib'

    hypodontia_stats = train_one_class_model(
        hypodontia_images,
        hypodontia_model_path,
        image_size=args.image_size,
        contamination=args.contamination,
    )
    discoloration_stats = train_one_class_model(
        discoloration_images,
        discoloration_model_path,
        image_size=args.image_size,
        contamination=args.contamination,
    )

    print('Training complete.')
    print('Hypodontia:', hypodontia_stats)
    print('Discoloration:', discoloration_stats)


if __name__ == '__main__':
    main()
