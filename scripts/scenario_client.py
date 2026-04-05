#!/usr/bin/env python3
"""Scenario API client with authentication and request helpers."""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import urllib.parse

BASE_URL = "https://api.cloud.scenario.com/v1"
MAX_RETRIES = 3
RETRY_DELAY = 2


class ScenarioClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.environ.get("SCENARIO_API_KEY")
        self.api_secret = api_secret or os.environ.get("SCENARIO_API_SECRET")
        if not self.api_key or not self.api_secret:
            print("Error: SCENARIO_API_KEY and SCENARIO_API_SECRET must be set.", file=sys.stderr)
            print("Run: export SCENARIO_API_KEY='your_key'", file=sys.stderr)
            print("Run: export SCENARIO_API_SECRET='your_secret'", file=sys.stderr)
            sys.exit(1)
        credentials = f"{self.api_key}:{self.api_secret}"
        self._auth_header = "Basic " + base64.b64encode(credentials.encode()).decode()

    def _request(self, method, path, params=None, json_body=None, retries=MAX_RETRIES):
        url = BASE_URL + path
        if params:
            query = urllib.parse.urlencode(params, doseq=True)
            url = f"{url}?{query}"

        headers = {
            "Authorization": self._auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = None
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    body = resp.read().decode("utf-8")
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="replace")
                if e.code == 429 and attempt < retries - 1:
                    wait = RETRY_DELAY * (attempt + 1)
                    print(f"Rate limited. Retrying in {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
                sys.exit(1)
            except urllib.error.URLError as e:
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                print(f"Connection error: {e.reason}", file=sys.stderr)
                sys.exit(1)

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, json_body=None, params=None):
        return self._request("POST", path, params=params, json_body=json_body or {})

    def put(self, path, json_body=None):
        return self._request("PUT", path, json_body=json_body or {})

    def delete(self, path, json_body=None):
        return self._request("DELETE", path, json_body=json_body or {})

    def poll_job(self, job_id, interval=3, max_wait=600):
        """Poll a job until it reaches a terminal state. Returns the job data."""
        elapsed = 0
        while elapsed < max_wait:
            data = self.get(f"/jobs/{job_id}")
            job = data.get("job", data)
            status = job.get("status", "unknown")
            progress = job.get("progress", 0)
            print(f"  Job {job_id}: status={status}, progress={progress}", file=sys.stderr)
            if status == "success":
                return job
            if status in ("failure", "canceled"):
                print(f"Job ended with status: {status}", file=sys.stderr)
                sys.exit(1)
            time.sleep(interval)
            elapsed += interval
        print(f"Job timed out after {max_wait}s", file=sys.stderr)
        sys.exit(1)

    def download_url(self, url, output_path):
        """Download a file from a URL to a local path."""
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        return output_path
