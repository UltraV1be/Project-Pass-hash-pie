import sys
import os
import hashlib
from unittest.mock import patch

# Adjust sys.path to find main modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from modules.breach_checker import check_password_breach


def test_breach_not_found():
    # Calculate SHA1 for a secure password
    pwd = "SomeHighlySecureUncompromisedPassword!2026"
    sha1 = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Mock get_suffix_list to return other suffixes, but not our suffix
    mock_response = [
        "ABCDEF1234567890ABCDEF1234567890ABC:4",
        "FEEBA1234567890ABCDEF1234567890ABCD:10",
    ]

    with patch(
        "services.hibp_service.HIBPServiceClient.get_suffix_list",
        return_value=mock_response,
    ):
        count = check_password_breach(pwd)
        assert count == 0


def test_breach_found():
    pwd = "password123"
    sha1 = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Mock get_suffix_list to return our suffix
    mock_response = [f"{suffix}:4532", "ABCDEF1234567890ABCDEF1234567890ABC:4"]

    with patch(
        "services.hibp_service.HIBPServiceClient.get_suffix_list",
        return_value=mock_response,
    ):
        count = check_password_breach(pwd)
        assert count == 4532
