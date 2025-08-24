# robot_keywords.py

import os
import json
from grafana_api import GrafanaAPI
from snapshot_comparator import normalize_output, compare_outputs
from utils import log_json, save_to_file

class GrafanaRegressionKeywords:
    def __init__(self):
        self.api = None
        self.snapshot_dir = None
        self.loader = None

    # 🧪 Grafana Interaction
    def set_grafana_credentials(self, url, token):
        self.api = GrafanaAPI(url, token)

    def fetch_panel_output(self, dashboard_uid, panel_id):
        return self.api.query_panel(dashboard_uid, panel_id)

    def get_panel_query(self, dashboard_uid, panel_id):
        dashboard_json = self.api.get_dashboard(dashboard_uid)
        return self.api.get_panel_query(dashboard_json, panel_id)

    def get_dashboard_panels(self, dashboard_uid):
        dashboard_json = self.api.get_dashboard(dashboard_uid)
        return dashboard_json['dashboard']['panels']

    def normalize_panel_output(self, output):
        return normalize_output(output)

    def compare_panel_output_to_snapshot(self, dashboard_uid, panel_id, dashboard_name):
        current = self.fetch_panel_output(dashboard_uid, panel_id)
        expected = self.load_snapshot_output(dashboard_name, panel_id)
        return compare_outputs(current, expected)

    def assert_panel_output_matches_snapshot(self, dashboard_uid, panel_id, dashboard_name):
        diff = self.compare_panel_output_to_snapshot(dashboard_uid, panel_id, dashboard_name)
        if diff:
            raise AssertionError(f"Panel output does not match snapshot:\n{diff}")

    def compare_multiple_panels_to_snapshots(self, dashboard_uid, dashboard_name):
        panels = self.get_dashboard_panels(dashboard_uid)
        mismatches = []
        for panel in panels:
            panel_id = panel['id']
            diff = self.compare_panel_output_to_snapshot(dashboard_uid, panel_id, dashboard_name)
            if diff:
                mismatches.append((panel_id, diff))
        if mismatches:
            raise AssertionError(f"Mismatches found:\n{mismatches}")


    # 🛠️ Utility & Debugging
    def log_panel_output(self, dashboard_uid, panel_id):
        output = self.fetch_panel_output(dashboard_uid, panel_id)
        log_json(output)

    def save_panel_output_to_file(self, dashboard_uid, panel_id, path):
        output = self.fetch_panel_output(dashboard_uid, panel_id)
        save_to_file(output, path)

    def diff_panel_outputs(self, dashboard_uid, panel_id, dashboard_name):
        current = self.fetch_panel_output(dashboard_uid, panel_id)
        expected = self.load_snapshot_output(dashboard_name, panel_id)
        diff = compare_outputs(current, expected)
        log_json(diff)

    def print_snapshot_metadata(self, dashboard_name):
        path = os.path.join(self.snapshot_dir, dashboard_name, "meta.yaml")
        if os.path.exists(path):
            with open(path) as f:
                print(f.read())
        else:
            print("No metadata found.")
