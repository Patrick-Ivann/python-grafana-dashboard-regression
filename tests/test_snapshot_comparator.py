import unittest
from deepdiff import DeepDiff
from snapshot_comparator import normalize_output, compare_outputs 


class TestOutputComparison(unittest.TestCase):

    def test_normalize_output_removes_timestamp(self):
        data = [
            {"value": 100, "timestamp": "2025-08-24T19:00:00Z"},
            {"value": 200, "timestamp": "2025-08-24T19:01:00Z"},
        ]
        expected = [{"value": 100}, {"value": 200}]
        result = normalize_output(data)
        self.assertEqual(result, expected)

    def test_normalize_output_with_no_timestamp(self):
        data = [{"value": 42}, {"value": 84}]
        result = normalize_output(data)
        self.assertEqual(result, data)

    def test_compare_outputs_equal(self):
        current = [
            {"value": 1, "timestamp": "2025-08-24T19:00:00Z"},
            {"value": 2, "timestamp": "2025-08-24T19:01:00Z"},
        ]
        expected = [
            {"value": 2, "timestamp": "2025-08-24T19:02:00Z"},
            {"value": 1, "timestamp": "2025-08-24T19:03:00Z"},
        ]
        diff = compare_outputs(current, expected)
        self.assertEqual(diff, {})  # No difference after normalization

    def test_compare_outputs_detects_difference(self):
        current = [{"value": 1, "timestamp": "2025-08-24T19:00:00Z"}]
        expected = [{"value": 2, "timestamp": "2025-08-24T19:01:00Z"}]
        diff = compare_outputs(current, expected)
        self.assertIn("values_changed", diff)

    def test_compare_outputs_empty_lists(self):
        current = []
        expected = []
        diff = compare_outputs(current, expected)
        self.assertEqual(diff, {})

    def test_compare_outputs_missing_field(self):
        current = [{"value": 1, "extra": "foo", "timestamp": "2025-08-24T19:00:00Z"}]
        expected = [{"value": 1, "timestamp": "2025-08-24T19:01:00Z"}]
        diff = compare_outputs(current, expected)
        self.assertIn("dictionary_item_added", diff)


if __name__ == "__main__":
    unittest.main()
