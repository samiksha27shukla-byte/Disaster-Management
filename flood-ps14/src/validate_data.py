"""Basic schema and quality validation."""
import pandas as pd
from src.data_loader import FEATURES, load_data

REQUIRED = ["zone_id", "day", "population", "lat", "lon", "flooded"] + FEATURES


def validate(df: pd.DataFrame) -> list[str]:
    issues = [f"missing column: {c}" for c in REQUIRED if c not in df.columns]
    if issues:
        return issues
    if df[REQUIRED].isnull().any().any():
        issues.append("null values present")
    if (df["rainfall_mm"] < 0).any():
        issues.append("negative rainfall")
    if not df["flooded"].isin([0, 1]).all():
        issues.append("flooded must be 0/1")
    if not df["soil_saturation"].between(0, 1).all():
        issues.append("soil_saturation out of [0,1]")
    return issues


if __name__ == "__main__":
    problems = validate(load_data())
    print("Data OK" if not problems else "\n".join(problems))
