import string
import math


class GraphDataService:
    """
    Prepares metadata structures for Chart.js frontend visualization.
    """

    @classmethod
    def get_character_distribution(cls, password):
        """
        Analyzes the password and yields counts of each character category.
        """
        distribution = {
            "labels": [
                "Lowercase",
                "Uppercase",
                "Digits",
                "Special Symbols",
                "Extended/Other",
            ],
            "values": [0, 0, 0, 0, 0],
        }

        if not password:
            return distribution

        special_chars = set(string.punctuation)

        for char in password:
            if char.islower():
                distribution["values"][0] += 1
            elif char.isupper():
                distribution["values"][1] += 1
            elif char.isdigit():
                distribution["values"][2] += 1
            elif char in special_chars:
                distribution["values"][3] += 1
            else:
                distribution["values"][4] += 1

        return distribution

    @classmethod
    def get_entropy_growth_curve(cls, password):
        """
        Generates simulated entropy values across increasing lengths,
        assuming the same character pool size.
        This illustrates the difference between short and long passwords visually.
        """
        curve = {"lengths": [], "entropies": []}

        if not password:
            return curve

        # Determine the pool size of the current password
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digits = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        pool_size = 0
        if has_lowercase:
            pool_size += 26
        if has_uppercase:
            pool_size += 26
        if has_digits:
            pool_size += 10
        if has_special:
            pool_size += 33

        if pool_size == 0:
            pool_size = 26  # Default minimum pool size to draw a curve

        # Calculate for lengths from 4 to 24
        for length in range(4, 25, 2):
            entropy = length * math.log2(pool_size)
            curve["lengths"].append(length)
            curve["entropies"].append(round(entropy, 2))

        return curve
