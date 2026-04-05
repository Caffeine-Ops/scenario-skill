#!/usr/bin/env python3
"""List and search assets in your Scenario project.

Usage:
  python3 list_assets.py
  python3 list_assets.py --type inference-txt2img --page-size 10
  python3 list_assets.py --model-id <model_id>
  python3 list_assets.py --tags "sci-fi,landscape" --privacy public
  python3 list_assets.py --created-after 2024-01-01T00:00:00Z
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenario_client import ScenarioClient


def main():
    parser = argparse.ArgumentParser(description="List Scenario assets")
    parser.add_argument("--type", help="Asset type filter (e.g., inference-txt2img, uploaded)")
    parser.add_argument("--types", nargs="+", help="Multiple asset types")
    parser.add_argument("--model-id", help="Filter by model ID")
    parser.add_argument("--inference-id", help="Filter by inference ID")
    parser.add_argument("--author-id", help="Filter by author ID")
    parser.add_argument("--parent-asset-id", help="Filter by parent asset ID")
    parser.add_argument("--root-asset-id", help="Filter by root asset ID")
    parser.add_argument("--collection-id", help="Filter by collection ID")
    parser.add_argument("--privacy", choices=["private", "public", "unlisted"],
                        help="Filter by privacy level")
    parser.add_argument("--tags", help="Comma-separated tags (public assets only)")
    parser.add_argument("--sort-by", choices=["createdAt", "updatedAt"],
                        help="Sort field")
    parser.add_argument("--sort-direction", choices=["asc", "desc"], help="Sort direction")
    parser.add_argument("--page-size", type=int, default=50, help="Items per page (1-100)")
    parser.add_argument("--pagination-token", help="Token for next page")
    parser.add_argument("--created-after", help="ISO date: assets created after")
    parser.add_argument("--created-before", help="ISO date: assets created before")
    parser.add_argument("--updated-after", help="ISO date: assets updated after")
    parser.add_argument("--updated-before", help="ISO date: assets updated before")
    parser.add_argument("--original", action="store_true", help="Return original assets")
    parser.add_argument("--all-pages", action="store_true",
                        help="Fetch all pages (caution: may be slow for large datasets)")
    parser.add_argument("--summary", action="store_true",
                        help="Print a human-readable summary instead of raw JSON")
    args = parser.parse_args()

    params = {}
    if args.type:
        params["type"] = args.type
    if args.types:
        params["types"] = args.types
    if args.model_id:
        params["modelId"] = args.model_id
    if args.inference_id:
        params["inferenceId"] = args.inference_id
    if args.author_id:
        params["authorId"] = args.author_id
    if args.parent_asset_id:
        params["parentAssetId"] = args.parent_asset_id
    if args.root_asset_id:
        params["rootAssetId"] = args.root_asset_id
    if args.collection_id:
        params["collectionId"] = args.collection_id
    if args.privacy:
        params["privacy"] = args.privacy
    if args.tags:
        params["tags"] = args.tags
    if args.sort_by:
        params["sortBy"] = args.sort_by
    if args.sort_direction:
        params["sortDirection"] = args.sort_direction
    if args.page_size:
        params["pageSize"] = str(min(max(args.page_size, 1), 100))
    if args.pagination_token:
        params["paginationToken"] = args.pagination_token
    if args.created_after:
        params["createdAfter"] = args.created_after
    if args.created_before:
        params["createdBefore"] = args.created_before
    if args.updated_after:
        params["updatedAfter"] = args.updated_after
    if args.updated_before:
        params["updatedBefore"] = args.updated_before
    if args.original:
        params["originalAssets"] = "true"

    client = ScenarioClient()

    all_assets = []
    page_count = 0

    while True:
        data = client.get("/assets", params=params)
        assets = data.get("assets", [])
        all_assets.extend(assets)
        page_count += 1
        next_token = data.get("nextPaginationToken")

        if not args.all_pages or not next_token:
            break

        params["paginationToken"] = next_token
        print(f"  Fetching page {page_count + 1}...", file=sys.stderr)

    if args.summary:
        print(f"\nFound {len(all_assets)} assets (page{'s' if page_count > 1 else ''}: {page_count})\n")
        for asset in all_assets:
            aid = asset.get("id", "?")
            kind = asset.get("kind", "?")
            atype = asset.get("metadata", {}).get("type", asset.get("type", "?"))
            status = asset.get("status", "?")
            created = asset.get("createdAt", "?")[:19]
            prompt = asset.get("metadata", {}).get("prompt", "")
            prompt_preview = (prompt[:60] + "...") if len(prompt) > 60 else prompt
            print(f"  {aid}  [{kind}/{atype}]  status={status}  created={created}")
            if prompt_preview:
                print(f"    prompt: {prompt_preview}")
        if data.get("nextPaginationToken"):
            print(f"\n  Next page token: {data['nextPaginationToken']}")
    else:
        output = {"assets": all_assets, "total": len(all_assets)}
        if data.get("nextPaginationToken") and not args.all_pages:
            output["nextPaginationToken"] = data["nextPaginationToken"]
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
