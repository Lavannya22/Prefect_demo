# cron_simulator.py — simulates cron firing every 10 seconds
import time
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT   = os.path.join(BASE_DIR, "etl.py")

print("Cron simulator started — firing etl.py every 10 seconds")
print("=" * 55)

RUN_COUNT = 3

for i in range(RUN_COUNT):
    print(f"\n[CRON] Run {i+1}/{RUN_COUNT} firing at {time.strftime('%H:%M:%S')}")
    subprocess.run(["python", SCRIPT])
    if i < RUN_COUNT - 1:
        print(f"[CRON] Done. Waiting 10 seconds...")
        time.sleep(10)

print()
print("=" * 55)
print("DEMO COMPLETE — Pipeline failed 3 times.")
print("Phase 1 repeated 3 times — all wasted.")
print("Phase 2 never succeeded. Phase 3 never ran.")
print("Zero retries. Zero cache. Zero recovery.")
print("=" * 55)
