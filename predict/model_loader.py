from .constants import MODEL_RANDOM_FOREST_REGRESSOR
import joblib
from .constants import ENCODER_BRAND, ENCODER_FUEL, ENCODER_MODEL, ENCODER_GEAR

# Carregando o modelo
model_random_forest_regressor = joblib.load(MODEL_RANDOM_FOREST_REGRESSOR, mmap_mode="r")

# Carregando os encoders
encoder_brand = joblib.load(ENCODER_BRAND, mmap_mode="r")
encoder_fuel = joblib.load(ENCODER_FUEL, mmap_mode="r")
encoder_model = joblib.load(ENCODER_MODEL, mmap_mode="r")
encoder_gear = joblib.load(ENCODER_GEAR, mmap_mode="r")
