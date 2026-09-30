"""Evacuation routing on a zone graph avoiding flooded zones."""
import math
import networkx as nx


def build_graph(zones_df, k=4):
    g = nx.Graph()
    pts = zones_df[["zone_id", "lat", "lon", "flood_prob"]].to_dict("records")
    for p in pts:
        g.add_node(p["zone_id"], **p)
    for p in pts:
        near = sorted(pts, key=lambda q: math.dist((p["lat"], p["lon"]), (q["lat"], q["lon"])))[1:k + 1]
        for q in near:
            d = math.dist((p["lat"], p["lon"]), (q["lat"], q["lon"])) * 111
            risk = (p["flood_prob"] + q["flood_prob"]) / 2
            g.add_edge(p["zone_id"], q["zone_id"], km=d, cost=d * (1 + 5 * risk))
    return g


def safest_route(g, src, shelters):
    best = None
    for s in shelters:
        try:
            path = nx.shortest_path(g, src, s, weight="cost")
            cost = nx.path_weight(g, path, "cost")
            if best is None or cost < best[1]:
                best = (path, cost)
        except nx.NetworkXNoPath:
            continue
    return best
