#Human readable duration format
def format_duration(seconds):
    if seconds == 0:
        return "now"

    units = [
        ("year", 365 * 24 * 60 * 60),
        ("day", 24 * 60 * 60),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1)
    ]

    parts = []

    for name, value in units:
        count = seconds // value

        if count:
            seconds %= value
            parts.append(f"{count} {name}" + ("s" if count > 1 else ""))

    if len(parts) == 1:
        return parts[0]

    return ", ".join(parts[:-1]) + " and " + parts[-1]