from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models" / "random_forest"

LOW_RISK_THRESHOLD = 70
HIGH_RISK_THRESHOLD = 90