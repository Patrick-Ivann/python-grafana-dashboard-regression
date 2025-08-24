import unittest
from unittest.mock import patch, Mock
from grafana_api import GrafanaAPI


class TestGrafanaAPI(unittest.TestCase):
    def setUp(self):
        self.api = GrafanaAPI("http://localhost:3000", "fake-token")

    @patch("grafana_api.requests.get")
    def test_get_dashboard(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"dashboard": {"title": "Test"}}
        mock_get.return_value = mock_response

        result = self.api.get_dashboard("abc123")
        self.assertEqual(result["dashboard"]["title"], "Test")

    @patch("grafana_api.requests.get")
    def test_get_dashboard_panels(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "dashboard": {"panels": [{"id": 1}, {"id": 2}]}
        }
        mock_get.return_value = mock_response

        panels = self.api.get_dashboard_panels("abc123")
        self.assertEqual(len(panels), 2)

    def test_get_panel_query(self):
        dashboard_json = {
            "dashboard": {
                "panels": [
                    {"id": 5, "targets": [{"refId": "A", "expr": "cpu_usage"}]}
                ]
            }
        }
        targets = self.api.get_panel_query(dashboard_json, 5)
        self.assertEqual(targets[0]["expr"], "cpu_usage")

    @patch("grafana_api.requests.post")
    def test_query_panel_prometheus(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": {"A": {"data": []}}}
        mock_post.return_value = mock_response

        targets = [{"refId": "A", "format": "time_series", "datasource": {"type": "prometheus"}}]
        result = self.api.query_panel("ds_uid", targets)
        self.assertIn("A", result["results"])


if __name__ == "__main__":
    unittest.main()
