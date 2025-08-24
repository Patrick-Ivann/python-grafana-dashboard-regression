# GrafanaAPI Python Client

A lightweight Python wrapper for interacting with Grafana's HTTP API. Supports Prometheus, Elasticsearch, and InfluxDB (InfluxQL and Flux).

## Features

- ✅ Fetch dashboards and panels
- 🔍 Extract panel queries
- 📊 Query panel data via Grafana backend

## Usage
```python
from grafana_api import GrafanaAPI

grafana = GrafanaAPI(base_url="http://localhost:3000", api_key="your_api_key")
grafana = GrafanaAPI(base_url="http://localhost:3000", username="admin", password="admin")

dashboard = grafana.get_dashboard("your_dashboard_uid")
panels = grafana.get_dashboard_panels("your_dashboard_uid")
targets = grafana.get_panel_query(dashboard, panel_id=1)
result = grafana.query_panel(datasource_uid="your_ds_uid", targets=targets)
```

