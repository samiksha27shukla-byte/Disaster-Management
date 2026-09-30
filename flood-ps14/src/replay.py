"""Replay a historical event day by day to show how risk evolves."""
from src.data_loader import FEATURES, load_data
from src.train_model import load_model


def replay(start=40, end=80, step=5):
    df, model = load_data(), load_model()
    timeline = []
    for d in range(start, end + 1, step):
        day = df[df.day == d]
        p = model.predict_proba(day[FEATURES])[:, 1]
        timeline.append({"day": d, "mean_prob": round(float(p.mean()), 3),
                         "zones_high": int((p > 0.6).sum()), "actual_flooded": int(day.flooded.sum())})
    return timeline


if __name__ == "__main__":
    for t in replay():
        print(t)
