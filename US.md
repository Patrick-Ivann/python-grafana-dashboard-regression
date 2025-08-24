✅ US-001: Initialize Python Package Structure

Description:
Detailed Description:
Create a modular Python library to serve as a Robot Framework backend. The structure should follow Python packaging best practices and allow for clear separation of logic: Grafana API, datasource loaders, snapshot comparison, Robot keyword bindings, and utilities.

This modular design will enable future extensibility, testing, and easier debugging.


Acceptance Criteria:

GIVEN the project root  
WHEN I run tree or inspect the repo 
THEN I should see a clear package layout with modules like grafana_api.py, robot_keywords.py, snapshot_loader.py, etc.

Example structure:
```
grafana_regression/
  ├── __init__.py
  ├── robot_keywords.py
  ├── grafana_api.py
  ├── snapshot_loader.py
  ├── snapshot_comparator.py
  ├── utils.py
  └── snapshots/
tests/
README.md
```

✅ US-002: Configure Grafana URL and API Token

Description:
Enable users to set the Grafana server URL and API token via keywords. These values are required to authenticate against the Grafana HTTP API.

All requests go to: ${GRAFANA_URL}/api/...

Requires Authorization: Bearer ${TOKEN} header

Add a keyword Test Grafana Connection that runs GET /api/user to validate credentials.

Acceptance Criteria:

GIVEN a Grafana URL and token   
WHEN I call Set Grafana Base URL and Set Grafana Credentials    
THEN all subsequent keywords should use this configuration to access the API.

Example usage in Robot:
```
Set Grafana Base URL    http://grafana.local
Set Grafana Credentials    ${GRAFANA_API_TOKEN}
```


✅ US-003: Create Save Current Panel Output As Snapshot logic

Description:
Query a panel’s datasource using its dashboard UID and panel ID, and store the raw response (timeseries or table) in a snapshot JSON file. This snapshot becomes the "expected result" for future comparisons.

Benefits:

Establishes a reference baseline

Snapshots can be version-controlled

Snapshots make future regression detection trivial

usefull Grafana API endpoints:
```
Endpoint: POST /api/ds/query
Construct body from panel query (from /api/dashboards/uid/:uid)
```

Request Body Example:
```
{
  "queries": [
    {
      "datasource": {"type": "influxdb", "uid": "influx"},
      "refId": "A",
      "rawSql": "SELECT mean(\"value\") FROM \"cpu\" WHERE $__timeFilter(time) GROUP BY time(1m)",
      "intervalMs": 60000
    }
  ],
  "range": {
    "from": "2024-01-01T00:00:00Z",
    "to": "2024-01-01T01:00:00Z"
  }
}
```

✅ US-004: Fetch and Normalize Panel Output

Detailed Description:
Queries a Grafana panel and normalizes its output for comparison. It handles:

Sorting timeseries by timestamp 
Rounding floats 
Removing volatile fields (like meta, or last scrape time)   

It would enable the possibility to Removes noise from comparisons, prevents false negatives in regression tests and normalize data based on these rules:
Round floats to 3 decimal places    
Sort .points[] in ascending time    
Strip metadata and rendering info   

Code Snippet (Python):
```
for series in data["series"]:
    series["points"] = sorted(series["points"])
    series["points"] = [[round(p[0], 3), p[1]] for p in series["points"]]
```

✅ US-007: Compare Panel Output To Snapshot

Detailed Description:
Compares the normalized live output of a Grafana panel to the corresponding saved snapshot. Fails the test if the results differ, and prints a readable diff.

Benefits:

Detects unintended changes in data

Prevents breaking dashboards due to backend changes

Pinpoints exact diff location in structured output

Robot Usage:

Compare Panel Output To Snapshot     dashboard_uid=abc123   panel_id=5


Python Tool:
Use deepdiff or jsondiff for structural comparison.


✅ US-009: Log and Diff Panel Outputs

Detailed Description:
On mismatch, produce a readable diff of the current vs. expected panel output   
Shows whether it's a rounding issue, missing label, etc.
output the diff in CLI print compatible (text) and in JSON
use deepdiff lib 