# etl.py — old way. No retry. No cache. Crashes on Phase 2.
import requests
import json
import time

def fetch_data():
    print(f"[PHASE 1] fetch_data() started at {time.strftime('%H:%M:%S')}")
    time.sleep(2)  # simulate API call
    res = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    res.raise_for_status()
    print("[PHASE 1] fetch_data() completed")
    return res.json()

def transform(data):
    print(f"[PHASE 2] transform() started at {time.strftime('%H:%M:%S')}")
    time.sleep(1)
    # Simulate ConnectionError to transform service
    raise ConnectionError("transform service unavailable (503)")

def save(data):
    print(f"[PHASE 3] save() started at {time.strftime('%H:%M:%S')}")
    with open("output.json", "w") as f:
        json.dump(data, f)
    print("[PHASE 3] save() completed — output.json written")

try:
    data      = fetch_data()
    transform(data)   # crashes here — no retry
    save(data)        # never runs
except Exception as e:
    print(f"[CRASH] {e}")
    print("[CRON]  No retry. No cache. All progress lost.")
