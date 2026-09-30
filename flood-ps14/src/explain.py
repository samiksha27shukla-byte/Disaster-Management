"""Simple explanations: global importances and per-zone contributions."""
import numpy as np
import pandas as pd
from src.data_loader import FEATURES


def global_importance(model) -> pd.Series:
    return pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)


def explain_row(model, row: pd.Series, baseline: pd.Series) -> dict:
    """Occlusion-style contribution: change in probability when each feature is set to baseline."""
    x = row[FEATURES].to_frame().T.astype(float)
    p = model.predict_proba(x)[0, 1]
    contrib = {}
    for f in FEATURES:
        x2 = x.copy()
        x2[f] = baseline[f]
        contrib[f] = round(float(p - model.predict_proba(x2)[0, 1]), 3)
    top = max(contrib, key=lambda k: abs(contrib[k]))
    return {"prob": round(float(p), 3), "contributions": contrib,
            "summary": f"Main driver: {top} ({contrib[top]:+.2f})"}
