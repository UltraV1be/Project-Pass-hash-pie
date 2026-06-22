import hashlib
import time
import secrets


def hash_password(password, salt=None, n=16384, r=8, p=1):
    """
    Hashes a password using Scrypt with configurable parameters.
    Parameters:
        n: CPU/memory cost factor (must be power of 2, e.g., 16384)
        r: Block size (e.g., 8)
        p: Parallelization (e.g., 1)
    """
    if salt is None:
        salt = secrets.token_hex(16)

    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")

    # Derivation key length
    dklen = 64

    # Calculate derived key
    derived_key = hashlib.scrypt(
        pwd_bytes, salt=salt_bytes, n=n, r=r, p=p, dklen=dklen
    )

    return f"{salt}${n}${r}${p}${derived_key.hex()}"


def verify_password(password, hashed_value):
    """
    Verifies a password against a Scrypt hash.
    """
    try:
        parts = hashed_value.split("$")
        if len(parts) != 5:
            return False

        salt, n_str, r_str, p_str, key_hex = parts
        n = int(n_str)
        r = int(r_str)
        p = int(p_str)

        test_hash = hash_password(password, salt=salt, n=n, r=r, p=p)
        return test_hash == hashed_value
    except Exception:
        return False


def benchmark_hash(password, n=16384, r=8, p=1):
    """
    Benchmarks Scrypt hashing execution speed.
    Returns:
        tuple: (hashed_value, elapsed_time_ms)
    """
    start_time = time.perf_counter()
    hashed = hash_password(password, n=n, r=r, p=p)
    elapsed = (time.perf_counter() - start_time) * 1000.0
    return hashed, round(elapsed, 4)
