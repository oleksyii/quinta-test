
from collections import defaultdict
from datetime import datetime, timezone

from constants import API_KEY, WORKSPACE_ID, BASE_URL, USER_ID, LOCAL_TZ, END_DATE, START_DATE
from http_client import HttpClient

from get_report import fetch_task_name
from util_functions.durations_formatters import format_duration
from util_functions.text_formatter import print_task, print_time_entry

http_client = HttpClient(API_KEY, BASE_URL)

def fetch_time_entries(start_date, end_date):
    page = 1
    time_entries = []

    while True:
        response = http_client.get(
            f"/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries",
            params={
                "start": start_date,
                "end": end_date,
                "page": page,
                "pageSize": 50,
            },
        )

        if not response:
            break  # Exit when no more data is returned

        time_entries.extend(response)
        page += 1

    return time_entries

def calculate_time_in_seconds(start, end):
    """Calculate time in seconds between two ISO datetime strings."""
    start_time = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
    end_time = (
        datetime.fromisoformat(end.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
        if end
        else datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    )
    duration = end_time - start_time
    return int(duration.total_seconds())

def get_all_task_entries(time_entries):
    """Group time entries by day and taskId, sum the durations, and return the grouped entries."""
    grouped_entries_by_task = defaultdict(list)

    for entry in time_entries:
        task_id = entry.get('taskId')
        start = entry['timeInterval']['start']
        end = entry['timeInterval'].get('end', None)
        description = entry.get('description', 'No Description')
        project_id = entry.get('projectId', None)
        task_name = fetch_task_name(project_id, task_id)
        duration_seconds = calculate_time_in_seconds(start, end)

        # Group by taskId
        grouped_entries_by_task[task_id].append({
            'task_name': task_name,
            'description': description,
            'start': start,
            'end': end,
            'duration_seconds': duration_seconds
        })

    return grouped_entries_by_task

def main():
    time_entries = fetch_time_entries(START_DATE, END_DATE)
    grouped_entries_by_task = get_all_task_entries(time_entries)

    # Display the total time for each task grouped by day
    for entries in grouped_entries_by_task.values():
        total_seconds = sum(entry["duration_seconds"] for entry in entries)
        total_duration_formatted = format_duration(total_seconds)

        task_name = entries[0]["task_name"]
        print_task(task_name, total_duration_formatted)

        # Print each time entry for the task on this day
        for entry in entries:
            print_time_entry(entry)


if __name__ == "__main__":
    main()