import hashlib
import time
import secrets


def hash_password(password, salt=None, iterations=1):
    """
    Hashes a password using SHA-512 with optional salt and custom loop iterations.
    """
    if salt is None:
        salt = secrets.token_hex(16)

    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")

    current_hash = hashlib.sha512(salt_bytes + pwd_bytes).digest()
    for _ in range(iterations - 1):
        current_hash = hashlib.sha512(current_hash).digest()

    return f"{salt}${iterations}${current_hash.hex()}"


def verify_password(password, hashed_value):
    """
    Verifies a password against an iterated SHA-512 hash.
    """
    try:
        parts = hashed_value.split("$")
        if len(parts) != 3:
            return False
        salt, iterations_str, hash_hex = parts
        iterations = int(iterations_str)

        test_hash = hash_password(password, salt=salt, iterations=iterations)
        return test_hash == hashed_value
    except Exception:
        return False


def benchmark_hash(password, iterations=1):
    """
    Benchmarks SHA-512 hashing execution speed.
    Returns:
        tuple: (hashed_value, elapsed_time_ms)
    """
    start_time = time.perf_counter()
    hashed = hash_password(password, iterations=iterations)
    elapsed = (time.perf_counter() - start_time) * 1000.0
    return hashed, round(elapsed, 4)
