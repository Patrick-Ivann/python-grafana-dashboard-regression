import json
from deepdiff import DeepDiff

def normalize_output(data):
    # Remove timestamps, volatile fields
    return [{k: v for k, v in item.items() if k != "timestamp"} for item in data]

def compare_outputs(current, expected):
    current_norm = normalize_output(current)
    expected_norm = normalize_output(expected)
    return DeepDiff(expected_norm, current_norm, ignore_order=True)
