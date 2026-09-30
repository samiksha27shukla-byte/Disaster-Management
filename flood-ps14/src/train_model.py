"""Train a flood-probability classifier."""
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
from src.data_loader import FEATURES, load_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "flood_model.pkl")


def train(df=None):
    df = load_data() if df is None else df
    split = int(df["day"].max() * 0.75)
    tr, te = df[df.day <= split], df[df.day > split]
    model = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=0, class_weight="balanced")
    model.fit(tr[FEATURES], tr["flooded"])
    proba = model.predict_proba(te[FEATURES])[:, 1]
    metrics = {"auc": float(roc_auc_score(te["flooded"], proba)) if te["flooded"].nunique() > 1 else None}
    print(classification_report(te["flooded"], proba > 0.5, zero_division=0))
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return model, metrics


def load_model():
    if not os.path.exists(MODEL_PATH):
        return train()[0]
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    print(train()[1])
