"""Synthetic data generation / loading for the flood prototype."""
import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def generate_synthetic(n_zones: int = 25, days: int = 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for z in range(n_zones):
        elevation = rng.uniform(2, 60)
        dist_river = rng.uniform(0.1, 10)
        soil = rng.uniform(0.2, 0.9)
        pop = int(rng.integers(500, 20000))
        lat, lon = 25.3 + rng.uniform(-0.2, 0.2), 82.9 + rng.uniform(-0.2, 0.2)
        level = rng.uniform(1, 3)
        for d in range(days):
            rain = max(0.0, rng.gamma(1.2, 12) * (1.8 if 40 < d < 80 else 0.6))
            level = 0.85 * level + 0.03 * rain + rng.normal(0, 0.1)
            risk = 0.04 * rain + 0.6 * level - 0.05 * elevation - 0.2 * dist_river + 2 * soil
            flood = int(risk + rng.normal(0, 0.5) > 2.5)
            rows.append(dict(zone_id=f"Z{z:02d}", day=d, rainfall_mm=round(rain, 2),
                             river_level_m=round(level, 3), elevation_m=round(elevation, 2),
                             dist_river_km=round(dist_river, 2), soil_saturation=round(soil, 3),
                             population=pop, lat=lat, lon=lon, flooded=flood))
    return pd.DataFrame(rows)


def load_data(path: str | None = None) -> pd.DataFrame:
    path = path or os.path.join(DATA_DIR, "flood_data.csv")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        generate_synthetic().to_csv(path, index=False)
    return pd.read_csv(path)


FEATURES = ["rainfall_mm", "river_level_m", "elevation_m", "dist_river_km", "soil_saturation"]
