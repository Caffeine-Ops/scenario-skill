#!/usr/bin/env python3
"""List available models in your Scenario project.

Usage:
  python3 get_models.py
  python3 get_models.py --public
  python3 get_models.py --status trained
  python3 get_models.py --summary
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenario_client import ScenarioClient


def main():
    parser = argparse.ArgumentParser(description="List Scenario models")
    parser.add_argument("--public", action="store_true", help="List public models")
    parser.add_argument("--status", help="Filter by status (e.g., trained, training)")
    parser.add_argument("--page-size", type=int, default=50, help="Items per page")
    parser.add_argument("--pagination-token", help="Token for next page")
    parser.add_argument("--summary", action="store_true",
                        help="Print human-readable summary")
    args = parser.parse_args()

    client = ScenarioClient()
    params = {"pageSize": str(min(max(args.page_size, 1), 100))}

    if args.pagination_token:
        params["paginationToken"] = args.pagination_token

    endpoint = "/models/public" if args.public else "/models"
    data = client.get(endpoint, params=params)
    models = data.get("models", [])

    if args.status:
        models = [m for m in models if m.get("status") == args.status]

    if args.summary:
        print(f"\nFound {len(models)} models:\n")
        for m in models:
            mid = m.get("id", "?")
            name = m.get("name", "untitled")
            status = m.get("status", "?")
            privacy = m.get("privacy", "?")
            tags = ", ".join(m.get("tags", []))
            print(f"  {mid}")
            print(f"    name: {name}  status={status}  privacy={privacy}")
            if tags:
                print(f"    tags: {tags}")
        if data.get("nextPaginationToken"):
            print(f"\n  Next page token: {data['nextPaginationToken']}")
    else:
        output = {"models": models, "total": len(models)}
        if data.get("nextPaginationToken"):
            output["nextPaginationToken"] = data["nextPaginationToken"]
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()


