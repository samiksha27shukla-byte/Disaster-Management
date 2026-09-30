"""End-to-end pipeline: validate -> train -> predict -> respond."""
import json
from src.data_loader import FEATURES, load_data
from src.validate_data import validate
from src.train_model import train
from src.vulnerability import vulnerability_scores
from src.explain import global_importance, explain_row
from src.social_pipeline import synthetic_posts, aggregate
from src.routing import build_graph, safest_route
from src.resource_optimizer import allocate
from src.alerts import make_alerts


def run(day=None):
    df = load_data()
    issues = validate(df)
    if issues:
        raise SystemExit("Validation failed: " + "; ".join(issues))
    model, metrics = train(df)
    day = int(df.day.max() * 0.5) if day is None else day
    latest = df[df.day == day].reset_index(drop=True)
    vuln = vulnerability_scores(latest, model.predict_proba(latest[FEATURES])[:, 1])
    g = build_graph(vuln)
    shelters = vuln.nsmallest(3, "flood_prob")["zone_id"].tolist()
    routes = {}
    for z in vuln[vuln.tier == "HIGH"]["zone_id"]:
        r = safest_route(g, z, shelters)
        if r:
            routes[z] = r[0]
    top = latest[latest.zone_id == vuln.iloc[0].zone_id].iloc[0]
    result = {
        "day": day, "metrics": metrics,
        "importance": global_importance(model).round(3).to_dict(),
        "top_zone_explanation": explain_row(model, top, df[FEATURES].median()),
        "social_signals": aggregate(synthetic_posts(vuln.zone_id.tolist())),
        "routes": routes,
        "allocation": allocate(vuln).to_dict("records"),
        "alerts": make_alerts(vuln, routes),
        "vulnerability": vuln.assign(tier=vuln.tier.astype(str)).to_dict("records"),
    }
    return result


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "vulnerability"}, indent=2, default=str))
