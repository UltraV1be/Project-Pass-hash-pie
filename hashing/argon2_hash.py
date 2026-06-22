import time
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


def hash_password(password, time_cost=2, memory_cost=65536, parallelism=4):
    """
    Hashes a password using Argon2id with customizable complexity parameters.
    Parameters:
        time_cost: Number of iterations (e.g., 2)
        memory_cost: Memory usage in KiB (e.g., 65536)
        parallelism: Number of parallel threads (e.g., 4)
    """
    ph = PasswordHasher(
        time_cost=time_cost, memory_cost=memory_cost, parallelism=parallelism
    )
    return ph.hash(password)


def verify_password(password, hashed_value):
    """
    Verifies a password against an Argon2 hash.
    """
    ph = PasswordHasher()
    try:
        return ph.verify(hashed_value, password)
    except VerificationError:
        return False
    except Exception:
        return False


def benchmark_hash(password, time_cost=2, memory_cost=65536, parallelism=4):
    """
    Benchmarks Argon2 hashing execution speed.
    Returns:
        tuple: (hashed_value, elapsed_time_ms)
    """
    start_time = time.perf_counter()
    hashed = hash_password(
        password,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
    )
    elapsed = (time.perf_counter() - start_time) * 1000.0
    return hashed, round(elapsed, 4)
