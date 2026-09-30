"""Generate tiered alert messages."""
from datetime import datetime, timezone

MESSAGES = {
    "HIGH": "EVACUATE NOW: severe flood risk in {z}. Move to shelter {s}.",
    "MEDIUM": "WARNING: flood risk rising in {z}. Prepare to evacuate.",
}


def make_alerts(vuln_df, routes=None):
    routes = routes or {}
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    alerts = []
    for _, r in vuln_df.iterrows():
        tier = str(r["tier"])
        if tier in MESSAGES:
            shelter = routes.get(r["zone_id"], ["?"])[-1]
            alerts.append({"time": ts, "zone_id": r["zone_id"], "tier": tier,
                           "message": MESSAGES[tier].format(z=r["zone_id"], s=shelter)})
    return alerts
