import math


def format_time(seconds):
    """
    Converts a duration in seconds to a human-readable string.
    """
    if seconds < 1:
        return "Instant"

    # Time constants
    minute = 60
    hour = 3600
    day = 86400
    year = 31536000
    century = year * 100

    if seconds < minute:
        return f"{round(seconds)} second{'s' if round(seconds) != 1 else ''}"
    elif seconds < hour:
        minutes = round(seconds / minute)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < day:
        hours = round(seconds / hour)
        return f"{hours} hour{'s' if hours != 1 else ''}"
    elif seconds < year:
        days = round(seconds / day)
        return f"{days} day{'s' if days != 1 else ''}"
    elif seconds < century:
        years = round(seconds / year)
        return f"{years} year{'s' if years != 1 else ''}"
    else:
        centuries = seconds / century
        if centuries > 1e12:
            return "Trillions of centuries"
        elif centuries > 1e9:
            return "Billions of centuries"
        elif centuries > 1e6:
            return "Millions of centuries"
        else:
            return f"{round(centuries):,} centuries"


def estimate_crack_time(entropy):
    """
    Estimates the time to crack a password based on its entropy value.
    Scenarios:
    1. Online Attack (100 guesses/sec)
    2. Offline Fast Hashing (10,000,000,000 guesses/sec, e.g., SHA-256 on high-end GPUs)
    3. Offline Slow Hashing (100,000 guesses/sec, e.g., Bcrypt/Argon2 slow custom hardware)
    """
    if entropy <= 0:
        return {
            "online_seconds": 0.0,
            "online_readable": "Instant",
            "offline_fast_seconds": 0.0,
            "offline_fast_readable": "Instant",
            "offline_slow_seconds": 0.0,
            "offline_slow_readable": "Instant",
        }

    # Total guess search space
    search_space = math.pow(2, entropy)

    # In average, only half of search space needs to be searched
    average_guesses = search_space / 2

    # Scenario Speeds (Guesses per second)
    online_speed = 100
    offline_fast_speed = 1e10  # 10 GH/s
    offline_slow_speed = 1e5  # 100 kH/s

    online_seconds = average_guesses / online_speed
    offline_fast_seconds = average_guesses / offline_fast_speed
    offline_slow_seconds = average_guesses / offline_slow_speed

    return {
        "online_seconds": online_seconds,
        "online_readable": format_time(online_seconds),
        "offline_fast_seconds": offline_fast_seconds,
        "offline_fast_readable": format_time(offline_fast_seconds),
        "offline_slow_seconds": offline_slow_seconds,
        "offline_slow_readable": format_time(offline_slow_seconds),
    }
