from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_data_to_json

# Define the local timezone
local_tz = pendulum.timezone("America/New_York")

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineer.com",
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz),
    # "end_date": datetime(2027, 1, 1, tzinfo=local_tz)
}

with DAG(
    dag_id="youtube_video_stats_dag_produce_json",
    default_args=default_args,
    description="A DAG to extract YouTube video stats and save to JSON",
    schedule="0 14 * * *",  # Cron schedule to run daily
    catchup=False,  # Do not backfill
) as dag:

    # Task 1: Get the playlist ID for the channel
    playlist_id = get_playlist_id()

    # Task 2: Get video IDs from the playlist
    video_ids = get_video_ids(playlist_id)

    # Task 3: Extract video data for each video ID
    extract_video_data = extract_video_data(video_ids)

    # Task 4: Save the extracted data to a JSON file
    save_data_to_json_task = save_data_to_json(extract_video_data)

    #Define task dependencies
    playlist_id >> video_ids >> extract_video_data >> save_data_to_json_task