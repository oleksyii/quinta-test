from datetime import datetime, timedelta, timezone

n_days = int(input("How many days from now would you like to see the data for: "))

start_date = datetime.now() - timedelta(days=n_days)
end_date = datetime.now()

START_DATE = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
END_DATE = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

# Local timezone (will be determined automatically)
LOCAL_TZ = datetime.now(timezone.utc).astimezone().tzinfo