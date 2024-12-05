import os
import textwrap
from datetime import datetime
from constants import LOCAL_TZ
from .durations_formatters import format_duration

# Get terminal width
terminal_width = os.get_terminal_size().columns
half_terminal_width = max(20, terminal_width // 2)  # Ensure a minimum width of 20

def print_date(date):
    print(f"\nDate: {date}")
    print(f"{'=' * half_terminal_width}")

def print_task(task_name, total_duration):
    wrapped_task_name = textwrap.fill(task_name, half_terminal_width)
    print(f"\nTask: \n{wrapped_task_name}")
    print(f"Total Duration: {total_duration}")
    print(f"{'-' * (half_terminal_width // 2)}")

def print_time_entry(entry):

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