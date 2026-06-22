import requests
import logging

logger = logging.getLogger(__name__)


class HIBPServiceClient:
    """
    Dedicated client for HaveIBeenPwned Range API queries.
    """

    BASE_URL = "https://api.pwnedpasswords.com/range"
    TIMEOUT = 5

    @classmethod
    def get_suffix_list(cls, prefix_5_chars):
        """
        Queries HIBP API with a 5-character SHA-1 hash prefix.
        Returns a list of raw matching suffix lines from HIBP, or an empty list if failed.
        """
        url = f"{cls.BASE_URL}/{prefix_5_chars}"
        headers = {"User-Agent": "SecurePass-Intelligence-App/1.0"}

        try:
            response = requests.get(url, headers=headers, timeout=cls.TIMEOUT)
            if response.status_code == 200:
                return response.text.splitlines()
            else:
                logger.warning(
                    f"HIBP API returned error code: {response.status_code}"
                )
                return []
        except requests.RequestException as e:
            logger.error(f"Network error querying HIBP service: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in HIBP service query: {e}")
            return []
