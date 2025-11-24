import os
import joblib
from django.conf import settings

# 🎯 BASE_DIR sempre aponta para o diretório raiz do projeto
BASE = settings.BASE_DIR

# ============================
#   Caminhos corretos dos modelos
# ============================

MODEL_DECISION_TREE_REGRESSOR = os.path.join(
    BASE, "predict", "machine_learn", "models_trained", "model_dt.joblib"
)

MODEL_RANDOM_FOREST_REGRESSOR = os.path.join(
    BASE, "predict", "machine_learn", "models_trained", "model_rf.joblib"
)

MODEL_HIST_GRADIENT_BOOSTING_REGRESSOR = os.path.join(
    BASE, "predict", "machine_learn", "models_trained", "model_hgb.joblib"
)

MODEL_VOTING_REGRESSOR = os.path.join(
    BASE, "predict", "machine_learn", "models_trained", "model_voting.joblib"
)

# ============================
#   Caminhos corretos dos encoders
# ============================

ENCODER_BRAND = os.path.join(
    BASE, "predict", "machine_learn", "columns_encoded", "encoder_brand.pkl"
)

ENCODER_MODEL = os.path.join(
    BASE, "predict", "machine_learn", "columns_encoded", "encoder_model.pkl"
)

ENCODER_FUEL = os.path.join(
    BASE, "predict", "machine_learn", "columns_encoded", "encoder_fuel.pkl"
)

ENCODER_GEAR = os.path.join(
    BASE, "predict", "machine_learn", "columns_encoded", "encoder_gear.pkl"
)
