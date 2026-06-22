import sys
import os

# Adjust sys.path to find main modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from hashing import (
    sha256_hash,
    sha512_hash,
    bcrypt_hash,
    scrypt_hash,
    argon2_hash,
)


def test_sha256():
    pwd = "TestPassword"
    hashed = sha256_hash.hash_password(pwd, iterations=5)
    assert sha256_hash.verify_password(pwd, hashed) is True
    assert sha256_hash.verify_password("wrong", hashed) is False


def test_sha512():
    pwd = "TestPassword"
    hashed = sha512_hash.hash_password(pwd, iterations=5)
    assert sha512_hash.verify_password(pwd, hashed) is True
    assert sha512_hash.verify_password("wrong", hashed) is False


def test_bcrypt():
    pwd = "TestPassword"
    hashed = bcrypt_hash.hash_password(pwd, rounds=6)
    assert bcrypt_hash.verify_password(pwd, hashed) is True
    assert bcrypt_hash.verify_password("wrong", hashed) is False


def test_scrypt():
    pwd = "TestPassword"
    hashed = scrypt_hash.hash_password(pwd, n=1024, r=8, p=1)
    assert scrypt_hash.verify_password(pwd, hashed) is True
    assert scrypt_hash.verify_password("wrong", hashed) is False


def test_argon2():
    pwd = "TestPassword"
    hashed = argon2_hash.hash_password(
        pwd, time_cost=1, memory_cost=8192, parallelism=1
    )
    assert argon2_hash.verify_password(pwd, hashed) is True
    assert argon2_hash.verify_password("wrong", hashed) is False
