"""Run the full PS14 pipeline from the command line."""
import json
from src.run_all import run
from src.replay import replay

if __name__ == "__main__":
    r = run()
    print("== Metrics ==", r["metrics"])
    print("== Top explanation ==", r["top_zone_explanation"]["summary"])
    print("== Allocation ==")
    for a in r["allocation"]:
        print(" ", a)
    print("== Alerts ==")
    for a in r["alerts"][:10]:
        print(" ", a["tier"], a["message"])
    print("== Replay ==")
    print(json.dumps(replay(), indent=1))
