"""Allocate rescue resources (boats, teams) proportional to need via LP."""
import numpy as np
from scipy.optimize import linprog


def allocate(vuln_df, total_units=30, max_per_zone=6):
    need = (vuln_df["vulnerability"] * vuln_df["population"] / 1000).to_numpy()
    n = len(need)
    res = linprog(-need, A_ub=np.ones((1, n)), b_ub=[total_units],
                  bounds=[(0, max_per_zone)] * n, method="highs")
    units = np.floor(res.x + 1e-6).astype(int) if res.success else np.zeros(n, int)
    out = vuln_df[["zone_id", "vulnerability"]].copy()
    out["units"] = units
    return out[out.units > 0].reset_index(drop=True)
