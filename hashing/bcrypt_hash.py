import bcrypt
import time


def hash_password(password, rounds=12):
    """
    Hashes a password using Bcrypt with a configurable rounds factor.
    """
    # Cap rounds boundaries [4, 31] to avoid hanging the app
    rounds = max(4, min(31, rounds))

    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password, hashed_value):
    """
    Verifies a password against a Bcrypt hash.
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_value.encode("utf-8")
        )
    except Exception:
        return False


def benchmark_hash(password, rounds=12):
    """
    Benchmarks Bcrypt hashing execution speed.
    Returns:
        tuple: (hashed_value, elapsed_time_ms)
    """
    start_time = time.perf_counter()
    hashed = hash_password(password, rounds=rounds)
    elapsed = (time.perf_counter() - start_time) * 1000.0
    return hashed, round(elapsed, 4)
