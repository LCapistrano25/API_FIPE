from functools import lru_cache
import joblib
from .constants import (
    MODEL_RANDOM_FOREST_REGRESSOR,
    MODEL_DECISION_TREE_REGRESSOR,
    MODEL_HIST_GRADIENT_BOOSTING_REGRESSOR,
    ENCODER_BRAND,
    ENCODER_FUEL,
    ENCODER_MODEL,
    ENCODER_GEAR,
)

@lru_cache(maxsize=1)
def get_model_random_forest_regressor():
    return joblib.load(MODEL_RANDOM_FOREST_REGRESSOR, mmap_mode="r")

@lru_cache(maxsize=1)
def get_model_decision_tree_regressor():
    return joblib.load(MODEL_DECISION_TREE_REGRESSOR, mmap_mode="r")

@lru_cache(maxsize=1)
def get_model_hist_gradient_boosting_regressor():
    return joblib.load(MODEL_HIST_GRADIENT_BOOSTING_REGRESSOR, mmap_mode="r")



@lru_cache(maxsize=1)
def get_encoder_brand():
    return joblib.load(ENCODER_BRAND, mmap_mode="r")

@lru_cache(maxsize=1)
def get_encoder_fuel():
    return joblib.load(ENCODER_FUEL, mmap_mode="r")

@lru_cache(maxsize=1)
def get_encoder_model():
    return joblib.load(ENCODER_MODEL, mmap_mode="r")

@lru_cache(maxsize=1)
def get_encoder_gear():
    return joblib.load(ENCODER_GEAR, mmap_mode="r")
