import requests
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import textwrap
import os
import pytz

# Set up your API key and workspace/user IDs
API_KEY = "OThjMTU0NWMtOGM2OC00NjA0LWFiNDktNGRkN2M2YThmYjQ4"
WORKSPACE_ID = "675097d574e04f76ec343efc"
USER_ID = "675097d574e04f76ec343efd"
BASE_URL = "https://api.clockify.me/api/v1"

# Specify the time range
START_DATE = "2024-01-01T00:00:00Z"  # Start date (ISO format)
END_DATE = "2024-12-31T23:59:59Z"  # End date (ISO format)

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json",
}

# Local timezone (can be changed to any valid timezone)
LOCAL_TZ = pytz.timezone("Europe/Kiev")


def fetch_time_entries(start_date, end_date):
    page = 1
    time_entries = []

    while True:
        response = requests.get(
            f"{BASE_URL}/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries",
            headers=headers,
            params={
                "start": start_date,
                "end": end_date,
                "page": page,
                "pageSize": 50,
            },
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.json()}")
            break

        response_data = response.json()
        if not response_data:
            break  # Exit when no more data is returned

        time_entries.extend(response_data)
        page += 1

    return time_entries


def fetch_task_name(project_id, task_id):
    """Fetch the task name from the project and task IDs."""
    if not project_id or not task_id:
        return "No Task"
    response = requests.get(
        f"{BASE_URL}/workspaces/{WORKSPACE_ID}/projects/{project_id}/tasks/{task_id}",
        headers=headers,
    )
    if response.status_code == 200:
        task_data = response.json()
        return task_data.get("name", "Unknown Task")
    else:
        return "Unknown Task"


def calculate_time_in_seconds(start, end):
    """Calculate time in seconds between two ISO datetime strings."""
    # Parse start and end times as offset-aware datetime objects
    start_time = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
    end_time = (
        datetime.fromisoformat(end.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
        if end
        else datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    )
    duration = end_time - start_time
    return int(duration.total_seconds())


def format_duration(seconds):
    """Format duration from seconds into minutes and seconds."""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes} min {remaining_seconds} sec"


def get_all_task_entries(time_entries):
    """Group time entries by day and taskId, sum the durations, and return the grouped entries."""
    grouped_entries_by_day = defaultdict(lambda: defaultdict(list))

    for entry in time_entries:
        task_id = entry.get('taskId')
        start = entry['timeInterval']['start']
        end = entry['timeInterval'].get('end', None)
        description = entry.get('description', 'No Description')
        project_id = entry.get('projectId', None)
        task_name = fetch_task_name(project_id, task_id)
        duration_seconds = calculate_time_in_seconds(start, end)

        # Extract the date part of the start time for grouping by day
        start_time = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
        date_key = start_time.date()

        # Group by day and taskId
        grouped_entries_by_day[date_key][task_id].append({
            'task_name': task_name,
            'description': description,
            'start': start,
            'end': end,
            'duration_seconds': duration_seconds
        })

    return grouped_entries_by_day


def main():
    # Fetch time entries
    time_entries = fetch_time_entries(START_DATE, END_DATE)

    # Get all task entries grouped by day and taskId
    grouped_entries_by_day = get_all_task_entries(time_entries)

    # Get terminal width
    terminal_width = os.get_terminal_size().columns
    half_terminal_width = max(20, terminal_width // 2)  # Ensure a minimum width of 20

    # Display the total time for each task grouped by day
    for date, task_groups in sorted(grouped_entries_by_day.items()):
        print(f"\nDate: {date}")
        print(f"{'=' * half_terminal_width}")

        # Calculate and display the total duration for each task on this day
        for task_id, entries in task_groups.items():
            total_seconds = sum(entry["duration_seconds"] for entry in entries)
            total_duration_formatted = format_duration(total_seconds)

            # Print the task header
            task_name = entries[0]["task_name"]
            wrapped_task_name = textwrap.fill(task_name, half_terminal_width)
            print(f"\nTask: \n{wrapped_task_name}")
            print(f"Total Duration: {total_duration_formatted}")
            print(f"{'-' * (half_terminal_width // 2)}")

            # Print each entry for the task on this day
            for entry in entries:
                duration_formatted = format_duration(entry["duration_seconds"])

                # Convert start and end times to local timezone and remove timezone info
                start_time = datetime.fromisoformat(entry['start'].replace("Z", "+00:00")).astimezone(LOCAL_TZ)
                end_time = datetime.fromisoformat(entry['end'].replace("Z", "+00:00")).astimezone(LOCAL_TZ) if entry['end'] else None

                start_time_str = start_time.strftime("%H:%M:%S")
                end_time_str = end_time.strftime("%H:%M:%S") if end_time else "Ongoing"

                print(f"  Start: {start_time_str}")
                print(f"  End: {end_time_str}")
                print(f"  Description: {entry['description']}")
                print(f"  Duration: {duration_formatted}")
                print("-" * (half_terminal_width // 2))  # Separator for each entry


if __name__ == "__main__":
    main()
