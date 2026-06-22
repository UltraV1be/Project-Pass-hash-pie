import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")


def get_dataset_path(filename):
    """
    Returns the absolute path to a dataset file.
    """
    return os.path.join(DATASETS_DIR, filename)


def load_wordlist(filename):
    """
    Loads a dataset file and returns a list of cleaned, lowercase lines.
    """
    path = get_dataset_path(filename)
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        # Strip lines and ignore comments or empty lines
        return [
            line.strip().lower()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def load_wordlist_set(filename):
    """
    Loads a dataset file and returns a set of cleaned, lowercase lines (for O(1) lookups).
    """
    return set(load_wordlist(filename))
