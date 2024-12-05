from datetime import datetime, timezone
from collections import defaultdict

from http_client import HttpClient
from constants import API_KEY, WORKSPACE_ID, USER_ID, BASE_URL, START_DATE, END_DATE, LOCAL_TZ
from util_functions import format_duration, print_date, print_task, print_time_entry

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


def fetch_task_name(project_id, task_id):
    """Fetch the task name from the project and task IDs."""
    if not project_id or not task_id:
        return "No Task"
    response = http_client.get(
        f"/workspaces/{WORKSPACE_ID}/projects/{project_id}",
    )
    return response.get("name", "Unknown Task")
    


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
    time_entries = fetch_time_entries(START_DATE, END_DATE)
    grouped_entries_by_day = get_all_task_entries(time_entries)

    # Display the total time for each task grouped by day
    for date, task_groups in sorted(grouped_entries_by_day.items()):
        print_date(date)

        # Calculate and display the total duration for each task on this day
        for entries in task_groups.values():
            total_seconds = sum(entry["duration_seconds"] for entry in entries)
            total_duration_formatted = format_duration(total_seconds)

            task_name = entries[0]["task_name"]
            print_task(task_name, total_duration_formatted)

            # Print each time entry for the task on this day
            for entry in entries:
                print_time_entry(entry)


if __name__ == "__main__":
    main()
