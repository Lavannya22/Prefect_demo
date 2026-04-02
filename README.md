# Prefect Demo — Cron vs Prefect

**Shruti Deulgaokar · Ashish Wagle · Lavannya Patil**

> *"Cron runs your script. Prefect runs your pipeline."*

---

## What This Demo Shows

A 3-step ETL pipeline that breaks in the real world:

- **Phase 1** — `fetch_data()` — calls an API, succeeds, result cached
- **Phase 2** — `transform()` — hits a `ConnectionError`, Prefect retries automatically, environment recovers on attempt 3
- **Phase 3** — `save()` — writes output.json

**Cron:** crashes at Phase 2, loses everything, restarts from scratch every time.  
**Prefect:** retries Phase 2 automatically, Phase 1 loaded from cache, pipeline completes. Zero manual intervention.

---

## Setup

### Step 1 — Install dependencies

```bash
pip install prefect requests
```

### Step 2 — Login to Prefect Cloud

```bash
prefect cloud login
```

This opens your browser. Sign in at [app.prefect.cloud](https://app.prefect.cloud). It's free to get started.

### Step 3 — Create your demo folder

```powershell
mkdir "D:\Masters Course Work\BDA\Demo"
cd "D:\Masters Course Work\BDA\Demo"
```

---

## Running the Demo

### Old Way — Cron (3 silent failures)

```bash
python cron_simulator.py
```

What you'll see:
```
[CRON] Run 1/3 firing at 20:01:00
[CRON] Done. Waiting 10 seconds...

[CRON] Run 2/3 firing at 20:01:10
[CRON] Done. Waiting 10 seconds...

[CRON] Run 3/3 firing at 20:01:20
[CRON] Done. Waiting 10 seconds...

DEMO COMPLETE — Script failed 3 times. Was anyone notified? No.
No retries. No alerts. No logs. Just silence.
```

### New Way — Prefect (retry + cache + recovery)

```bash
python etl_prefect.py
```

What you'll see:
```
[PHASE 1] fetch_data() started
[PHASE 1] fetch_data() completed — result cached

[PHASE 2] transform() — attempt 1/3
[PHASE 2] ConnectionError: transform service unavailable (503)
Prefect: retrying automatically in 5s...

[PHASE 2] transform() — attempt 2/3
[PHASE 2] ConnectionError: transform service unavailable (503)
Prefect: retrying automatically in 5s...

[PHASE 2] transform() — attempt 3/3
[PHASE 2] transform service recovered. Processing...
[PHASE 2] transform() completed

[PHASE 3] save() completed — output.json written

Pipeline COMPLETED. Zero manual intervention.
```

Then open [app.prefect.cloud](https://app.prefect.cloud) to see the full run history, task states, retries, and logs in the UI.

---

## Setting Up Email Notifications

1. Go to [app.prefect.cloud](https://app.prefect.cloud)
2. Click **Automations** in the left sidebar
3. Click **Add Automation**
4. Set trigger: `Flow run state` → `Failed` or `Crashed`
5. Set action: `Send a notification` → `Email` → your email address
6. Click **Save**

> Note: Email notifications require a paid Prefect Cloud account. The free tier includes Slack notifications.

---

## The 5 Demo Framework Slides

| Slide | Section | What it covers |
|---|---|---|
| 1 | **Motivation** | Memory vs Compute vs Syntax — Syntax is the bottleneck |
| 2 | **The What** | @task, task_input_hash, @flow, Prefect Cloud UI |
| 3 | **The Demo** | Side-by-side code — patterns to steal |
| 4 | **AI Shift** | Embeddings, Feature Stores, Privacy-safe Training |
| 5 | **Bottom Line** | "Cron knows your script ran. Prefect knows if it worked." |

---

## Key Concepts

| Concept | What it means |
|---|---|
| `@task` | Wraps a function — adds retry, logging, caching |
| `@flow` | Wraps your main function — makes it an observable pipeline |
| `retries=3` | Automatically retry the task up to 3 times on failure |
| `retry_delay_seconds=5` | Wait 5 seconds between each retry |
| `cache_key_fn=task_input_hash` | Cache the result by input hash — skip on re-run if inputs unchanged |
| `log_prints=True` | Every print() statement appears in the Prefect Cloud UI |

---

## Why Prefect Over Cron

| | Cron | Prefect |
|---|---|---|
| Retries | ❌ None | ✅ Built-in |
| Failure alerts | ❌ Silent | ✅ Email / Slack |
| Caching | ❌ None | ✅ task_input_hash |
| Visibility | ❌ Zero | ✅ Full UI dashboard |
| Phase 1 on retry | ❌ Runs again | ✅ Loaded from cache |
| Code change needed | — | Two decorators |

---

## Live Demo Files

| File | What it is |
|---|---|
| `prefect_demo.html` | Full demo with 3 tabs — Code Comparison, Live Simulation, Run Locally |
| `prefect_sim.html` | Standalone simulation — Phase 1 caches, Phase 2 retries, Phase 3 completes |

Open either file directly in your browser. No server needed.

---

## Prefect Cloud Links

- Dashboard: [app.prefect.cloud](https://app.prefect.cloud)
- Docs: [docs.prefect.io](https://docs.prefect.io)
- Alerts tutorial: [docs.prefect.io/v3/tutorials/alerts](https://docs.prefect.io/v3/tutorials/alerts)

---

