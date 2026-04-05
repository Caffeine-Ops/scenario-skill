#!/usr/bin/env python3
"""Download assets from Scenario to local filesystem.

Usage:
  python3 download_asset.py --asset-id <id> --output ./downloads/
  python3 download_asset.py --asset-ids <id1> <id2> --output ./downloads/
  python3 download_asset.py --inference-id <id> --output ./downloads/
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenario_client import ScenarioClient


def download_single(client, asset_id, output_dir):
    """Download a single asset by ID."""
    data = client.get(f"/assets/{asset_id}")
    asset = data.get("asset", data)
    url = asset.get("url")
    if not url:
        print(f"No URL found for asset {asset_id}", file=sys.stderr)
        return None

    mime = asset.get("mimeType", "image/png")
    ext_map = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
        "image/svg+xml": "svg",
        "video/mp4": "mp4",
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "model/gltf-binary": "glb",
    }
    ext = ext_map.get(mime, mime.split("/")[-1] if "/" in mime else "bin")
    filename = f"{asset_id}.{ext}"
    out_path = os.path.join(output_dir, filename)

    client.download_url(url, out_path)
    size = os.path.getsize(out_path)
    print(f"Downloaded: {out_path} ({size:,} bytes)", file=sys.stderr)

    return {
        "assetId": asset_id,
        "path": out_path,
        "size": size,
        "mimeType": mime,
        "metadata": asset.get("metadata", {}),
    }


def main():
    parser = argparse.ArgumentParser(description="Download Scenario assets")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--asset-id", help="Single asset ID to download")
    group.add_argument("--asset-ids", nargs="+", help="Multiple asset IDs")
    group.add_argument("--inference-id",
                       help="Download all assets from an inference")
    parser.add_argument("--output", "-o", default="./downloads",
                        help="Output directory (default: ./downloads)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    client = ScenarioClient()

    asset_ids = []
    if args.asset_id:
        asset_ids = [args.asset_id]
    elif args.asset_ids:
        asset_ids = args.asset_ids
    elif args.inference_id:
        # Fetch all assets from this inference
        data = client.get("/assets", params={"inferenceId": args.inference_id})
        assets = data.get("assets", [])
        asset_ids = [a["id"] for a in assets]
        if not asset_ids:
            print(f"No assets found for inference {args.inference_id}", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(asset_ids)} assets for inference {args.inference_id}", file=sys.stderr)

    results = []
    for aid in asset_ids:
        result = download_single(client, aid, args.output)
        if result:
            results.append(result)

    print(json.dumps({"downloaded": results, "total": len(results)}, indent=2))


if __name__ == "__main__":
    main()
