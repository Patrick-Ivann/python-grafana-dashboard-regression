import logging
import requests
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GrafanaAPI:
    """Handles interaction with Grafana's HTTP API using API key or basic auth."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            })
            logger.info("Using API key authentication")
        elif username and password:
            self.session.auth = (username, password)
            self.session.headers.update({"Content-Type": "application/json"})
            logger.info("Using basic authentication with username/password")
        else:
            raise ValueError("Authentication required: provide either api_key or username/password")

    def get_dashboard(self, uid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/dashboards/uid/{uid}"
        logger.debug("GET %s", url)
        response = self.session.get(url)
        response.raise_for_status()
        logger.info("Dashboard %s retrieved", uid)
        return response.json()

    def get_dashboard_panels(self, uid: str) -> List[Dict[str, Any]]:
        dashboard = self.get_dashboard(uid)
        panels = dashboard.get("dashboard", {}).get("panels", [])
        logger.info("Found %d panels in dashboard %s", len(panels), uid)
        return panels

    def get_panel_query(self, dashboard_json: Dict[str, Any], panel_id: int) -> Optional[List[Dict[str, Any]]]:
        panels = dashboard_json.get("dashboard", {}).get("panels", [])
        for panel in panels:
            if panel.get("id") == panel_id:
                logger.info("Panel %d found", panel_id)
                return panel.get("targets", [])
        logger.warning("Panel %d not found", panel_id)
        return None

    def query_panel(self, datasource_uid: str, targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/ds/query"
        queries = []

        for target in targets:
            query_type = target.get("datasource", {}).get("type", "prometheus")
            ref_id = target.get("refId", "A")

            query = {
                "datasource": {"uid": datasource_uid},
                "refId": ref_id,
                "intervalMs": 60000,
                "maxDataPoints": 500,
                "format": target.get("format", "time_series"),
                "target": target,
            }

            if query_type == "elasticsearch":
                query.update({
                    "queryType": "lucene",
                    "timeField": "@timestamp",
                })
            elif query_type == "influxdb":
                query.update({
                    "queryType": target.get("queryType", "influxql"),  # influxql or flux
                })

            queries.append(query)

        payload = {"queries": queries}
        logger.debug("POST %s with payload: %s", url, payload)
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        logger.info("query executed for datasource %s", datasource_uid)
        return response.json()