from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, Tuple

import joblib
import numpy as np
from PIL import Image, ImageOps


MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')


class ModelNotAvailableError(RuntimeError):
	"""Raised when required model files are missing."""


def _image_to_vector(image_path: str, image_size: int = 96) -> np.ndarray:
	with Image.open(image_path) as img:
		img = ImageOps.exif_transpose(img)
		img = img.convert('L').resize((image_size, image_size))
	arr = np.asarray(img, dtype=np.float32) / 255.0
	return arr.reshape(1, -1)


@lru_cache(maxsize=1)
def _load_models() -> Dict[str, dict]:
	model_paths = {
		'hypodontia': os.path.join(MODELS_DIR, 'hypodontia_model.joblib'),
		'discoloration': os.path.join(MODELS_DIR, 'discoloration_model.joblib'),
	}

	missing = [name for name, path in model_paths.items() if not os.path.exists(path)]
	if missing:
		missing_names = ', '.join(missing)
		raise ModelNotAvailableError(
			f"Missing trained model(s): {missing_names}. Run train_models.py first."
		)

	return {name: joblib.load(path) for name, path in model_paths.items()}


def _score_with_model(image_path: str, model_bundle: dict) -> Tuple[bool, float]:
	x = _image_to_vector(image_path, image_size=model_bundle['image_size'])
	x_scaled = model_bundle['scaler'].transform(x)
	x_reduced = model_bundle['pca'].transform(x_scaled)

	score = float(model_bundle['isolation_forest'].decision_function(x_reduced)[0])
	threshold = float(model_bundle['threshold'])
	is_in_class = score >= threshold

	# Convert margin from threshold into a bounded confidence percentage.
	margin = score - threshold
	confidence = 50.0 + 50.0 * np.tanh(margin * 8.0)
	confidence = float(np.clip(confidence, 1.0, 99.0))
	if not is_in_class:
		confidence = 100.0 - confidence

	return is_in_class, confidence


def predict_condition(image_path: str, condition_type: str):
	"""Return (result, confidence, explanation) for uploaded image."""
	models = _load_models()

	normalized_type = (condition_type or '').strip().lower()
	if normalized_type not in {'hypodontia', 'discoloration'}:
		raise ValueError(f'Unsupported condition type: {condition_type}')

	is_in_class, confidence = _score_with_model(image_path, models[normalized_type])

	if normalized_type == 'hypodontia':
		if is_in_class:
			result = 'Hypodontia Pattern Detected'
			explanation = (
				'The uploaded X-ray is similar to the trained hypodontia pattern set.'
			)
		else:
			result = 'No Clear Hypodontia Pattern'
			explanation = (
				'The uploaded X-ray differs from the trained hypodontia pattern set.'
			)
	else:
		if is_in_class:
			result = 'Tooth Discoloration Pattern Detected'
			explanation = (
				'The uploaded photo is similar to the trained discoloration pattern set.'
			)
		else:
			result = 'No Clear Discoloration Pattern'
			explanation = (
				'The uploaded photo differs from the trained discoloration pattern set.'
			)

	return result, round(confidence, 2), explanation
