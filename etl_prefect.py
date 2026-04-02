# etl_prefect.py — Prefect handles cache, retry, and recovery
import requests
import json
import time
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

# Track retry attempts for the simulation
transform_attempts = {"count": 0}

@task(
    retries=3,
    retry_delay_seconds=5,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
    log_prints=True
)
def fetch_data():
    print(f"[PHASE 1] fetch_data() started at {time.strftime('%H:%M:%S')}")
    time.sleep(2)  # simulate API call
    res = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    res.raise_for_status()
    print("[PHASE 1] fetch_data() completed — result will be cached")
    return res.json()

@task(
    retries=3,
    retry_delay_seconds=5,
    log_prints=True
)
def transform(data):
    transform_attempts["count"] += 1
    attempt = transform_attempts["count"]
    print(f"[PHASE 2] transform() — attempt {attempt}/3")

    # Simulate: fails on attempt 1 and 2, recovers on attempt 3
    if attempt < 3:
        print(f"[PHASE 2] ConnectionError: transform service unavailable (503)")
        raise ConnectionError(f"transform service unavailable — attempt {attempt}")

    # Attempt 3 — environment recovered
    print("[PHASE 2] transform service recovered. Processing...")
    time.sleep(1)
    result = {"id": data["id"], "title": data["title"].upper()}
    print(f"[PHASE 2] transform() completed — {result}")
    return result

@task(log_prints=True)
def save(data):
    print(f"[PHASE 3] save() started at {time.strftime('%H:%M:%S')}")
    time.sleep(1)
    with open("output.json", "w") as f:
        json.dump(data, f)
    print("[PHASE 3] save() completed — output.json written")

@flow(name="ETL Pipeline", log_prints=True)
def etl_pipeline():
    print("=" * 55)
    print(f"Pipeline started at {time.strftime('%H:%M:%S')}")
    print("=" * 55)

    # Phase 1 — succeeds and is cached
    data = fetch_data()

    # Phase 2 — fails twice, recovers on attempt 3 automatically
    transformed = transform(data)

    # Phase 3 — runs after Phase 2 recovers
    save(transformed)

    print("=" * 55)
    print("Pipeline COMPLETED. Zero manual intervention.")
    print("=" * 55)

if __name__ == "__main__":
    etl_pipeline()
