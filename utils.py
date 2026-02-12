def parse_time(time_str):
    time_str = time_str.lower()
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        # Check if the last character is s, m, h, or d
        if time_str[-1] in units:
            return int(time_str[:-1]) * units[time_str[-1]]
        return int(time_str) # Default to seconds
    except:
        return None
