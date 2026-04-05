#!/usr/bin/env python3
"""Generate images via the Scenario API.

Supports txt2img, img2img, controlnet, inpaint, upscale, remove-background,
restyle, and vectorize modes.

Usage:
  python3 generate.py --prompt "a cute cat" --model-id flux.1-dev
  python3 generate.py --mode img2img --prompt "oil painting" --model-id sd-xl --image asset_xxx
  python3 generate.py --mode upscale --image asset_xxx
  python3 generate.py --mode remove-background --image asset_xxx
"""

import argparse
import json
import os
import sys
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenario_client import ScenarioClient


def load_image_as_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_payload(args):
    mode = args.mode
    payload = {}

    if args.prompt:
        payload["prompt"] = args.prompt
    if args.negative_prompt:
        payload["negativePrompt"] = args.negative_prompt
    if args.model_id:
        payload["modelId"] = args.model_id
    if args.num_samples:
        payload["numSamples"] = args.num_samples
    if args.guidance is not None:
        payload["guidance"] = args.guidance
    if args.steps:
        payload["numInferenceSteps"] = args.steps
    if args.width:
        payload["width"] = args.width
    if args.height:
        payload["height"] = args.height
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.scheduler:
        payload["scheduler"] = args.scheduler

    # Image reference (can be asset ID, file path, or data URL)
    if args.image:
        if os.path.isfile(args.image):
            payload["image"] = "data:image/png;base64," + load_image_as_base64(args.image)
        else:
            payload["image"] = args.image

    if args.mask:
        if os.path.isfile(args.mask):
            payload["mask"] = "data:image/png;base64," + load_image_as_base64(args.mask)
        else:
            payload["mask"] = args.mask

    if args.modality:
        payload["modality"] = args.modality
    if args.scaling_factor is not None:
        payload["scalingFactor"] = args.scaling_factor
    if args.creativity is not None:
        payload["creativity"] = args.creativity
    if args.style:
        payload["style"] = args.style
    if args.strength is not None:
        payload["strength"] = args.strength
    if args.image_fidelity is not None:
        payload["imageFidelity"] = args.image_fidelity
    if args.prompt_fidelity is not None:
        payload["promptFidelity"] = args.prompt_fidelity

    return payload


ENDPOINT_MAP = {
    "txt2img": "/generate/txt2img",
    "img2img": "/generate/img2img",
    "controlnet": "/generate/controlnet",
    "inpaint": "/generate/inpaint",
    "upscale": "/generate/upscale",
    "remove-background": "/generate/remove-background",
    "restyle": "/generate/restyle",
    "vectorize": "/generate/vectorize",
    "generative-fill": "/generate/generative-fill",
    "reframe": "/generate/reframe",
    "pixelate": "/generate/pixelate",
    "segment": "/generate/segment",
}


def main():
    parser = argparse.ArgumentParser(description="Generate images via Scenario API")
    parser.add_argument("--mode", default="txt2img", choices=list(ENDPOINT_MAP.keys()),
                        help="Generation mode (default: txt2img)")
    parser.add_argument("--prompt", help="Text prompt for generation")
    parser.add_argument("--negative-prompt", help="Negative prompt (SD models only)")
    parser.add_argument("--model-id", help="Model ID to use")
    parser.add_argument("--image", help="Input image: asset ID or local file path")
    parser.add_argument("--mask", help="Mask image: asset ID or local file path (for inpainting)")
    parser.add_argument("--modality", help="ControlNet modality (canny, depth, pose, etc.)")
    parser.add_argument("--scaling-factor", type=int, help="Upscale multiplier (1-16, for upscale mode)")
    parser.add_argument("--creativity", type=int, help="Creative freedom (0-100, for upscale/restyle)")
    parser.add_argument("--style", help="Style preset (anime, cartoon, cinematic, photo)")
    parser.add_argument("--strength", type=float, help="Transform strength (0-1, for img2img)")
    parser.add_argument("--image-fidelity", type=int, help="Preserve original (0-100, for restyle)")
    parser.add_argument("--prompt-fidelity", type=int, help="Follow prompt (0-100, for restyle)")
    parser.add_argument("--num-samples", type=int, default=1, help="Number of images (1-8)")
    parser.add_argument("--guidance", type=float, help="Guidance scale (default: 7.5 for SD, 3.5 for Flux)")
    parser.add_argument("--steps", type=int, help="Inference steps (5-50)")
    parser.add_argument("--width", type=int, help="Image width in pixels")
    parser.add_argument("--height", type=int, help="Image height in pixels")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--scheduler", help="Denoising scheduler")
    parser.add_argument("--no-poll", action="store_true", help="Don't poll job, just return job ID")
    parser.add_argument("--download", help="Directory to download results to")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")
    args = parser.parse_args()

    endpoint = ENDPOINT_MAP[args.mode]
    payload = build_payload(args)

    client = ScenarioClient()

    print(f"Generating with mode={args.mode}...", file=sys.stderr)
    response = client.post(endpoint, json_body=payload)

    if args.json and args.no_poll:
        print(json.dumps(response, indent=2))
        return

    job = response.get("job", {})
    job_id = job.get("jobId")

    if not job_id:
        print(json.dumps(response, indent=2))
        return

    print(f"Job created: {job_id}", file=sys.stderr)

    if args.no_poll:
        result = {"jobId": job_id, "status": job.get("status")}
        print(json.dumps(result, indent=2))
        return

    # Poll until completion
    completed_job = client.poll_job(job_id)
    asset_ids = completed_job.get("metadata", {}).get("assetIds", [])

    print(f"\nGeneration complete! Asset IDs: {asset_ids}", file=sys.stderr)

    # Optionally download
    if args.download and asset_ids:
        os.makedirs(args.download, exist_ok=True)
        for aid in asset_ids:
            asset_data = client.get(f"/assets/{aid}")
            asset = asset_data.get("asset", asset_data)
            url = asset.get("url")
            if url:
                mime = asset.get("mimeType", "image/png")
                ext = mime.split("/")[-1] if "/" in mime else "png"
                out_path = os.path.join(args.download, f"{aid}.{ext}")
                client.download_url(url, out_path)
                print(f"Downloaded: {out_path}", file=sys.stderr)

    # Output result
    output = {
        "jobId": job_id,
        "status": "success",
        "assetIds": asset_ids,
    }
    if args.json:
        output["job"] = completed_job
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
