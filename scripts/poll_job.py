#!/usr/bin/env python3
"""Poll a Scenario job until completion.

Usage:
  python3 poll_job.py --job-id <job_id>
  python3 poll_job.py --job-id <job_id> --interval 5 --timeout 300
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenario_client import ScenarioClient


def main():
    parser = argparse.ArgumentParser(description="Poll Scenario job status")
    parser.add_argument("--job-id", required=True, help="Job ID to poll")
    parser.add_argument("--interval", type=int, default=3,
                        help="Poll interval in seconds (default: 3)")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Max wait time in seconds (default: 600)")
    args = parser.parse_args()

    client = ScenarioClient()
    job = client.poll_job(args.job_id, interval=args.interval, max_wait=args.timeout)

    asset_ids = job.get("metadata", {}).get("assetIds", [])
    output = {
        "jobId": args.job_id,
        "status": job.get("status"),
        "assetIds": asset_ids,
        "jobType": job.get("jobType"),
        "progress": job.get("progress"),
        "createdAt": job.get("createdAt"),
        "updatedAt": job.get("updatedAt"),
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
