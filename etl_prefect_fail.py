from prefect import flow, task

@task(retries=3, retry_delay_seconds=5, log_prints=True)
def fetch_data():
    import requests
    res = requests.get("https://jsonplaceholder.typicode.com/posts/999999")
    res.raise_for_status()
    return res.json()

@flow(name="ETL Pipeline")
def etl_pipeline():
    fetch_data()  # retries, logs, alerts — all automatic

etl_pipeline()
