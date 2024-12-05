def format_duration(seconds):
    """Format duration from seconds into minutes and seconds."""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes} min {remaining_seconds} sec"