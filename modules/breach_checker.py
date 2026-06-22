import hashlib
import logging
from services.hibp_service import HIBPServiceClient

logger = logging.getLogger(__name__)


def check_password_breach(password):
    """
    Checks if a password has been leaked in a public data breach using the HIBP Range API.
    Uses k-Anonymity: sends only the first 5 characters of the SHA-1 hash.

    Returns:
        int: Number of times the password was breached, or 0 if not found.
    """
    if not password:
        return 0

    try:
        # Calculate SHA-1 hash
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        # Query HIBP service
        lines = HIBPServiceClient.get_suffix_list(prefix)

        for line in lines:
            if ":" in line:
                match_suffix, count_str = line.split(":", 1)
                if match_suffix == suffix:
                    return int(count_str)

        return 0

    except Exception as e:
        logger.error(f"Unexpected error in breach check: {e}")
        return 0
