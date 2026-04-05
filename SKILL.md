---
name: scenario
description: "Interact with the Scenario API to generate AI images, list/search/download assets, manage models, and automate creative workflows. Use this skill whenever the user mentions Scenario, wants to generate images via Scenario's platform, needs to retrieve or download AI-generated assets, list available models, check generation job status, or build any visual content pipeline with Scenario. Also use when the user references scenario.com, Scenario API keys, or asks about txt2img/img2img/ControlNet/inpainting generation through Scenario."
---

# Scenario API Skill

This skill provides full access to the Scenario API for AI-powered image generation, asset management, and model training. All operations go through `https://api.cloud.scenario.com/v1`.

## Authentication Setup

Scenario uses **HTTP Basic Auth**. The user needs two credentials stored as environment variables:

- `SCENARIO_API_KEY` — the API key from Scenario dashboard
- `SCENARIO_API_SECRET` — the API secret paired with the key

If these are not set, prompt the user to configure them:

```bash
export SCENARIO_API_KEY="your_api_key"
export SCENARIO_API_SECRET="your_api_secret"
```

All scripts in `scripts/` read these env vars automatically. Never hardcode credentials.

## Core Workflows

### 1. Generate Images (Most Common)

Image generation is **asynchronous** — you submit a request, get a `jobId`, then poll until completion.

**Step-by-step:**

1. Run the generation script with desired parameters:
   ```bash
   python3 SKILL_DIR/scripts/generate.py \
     --prompt "a futuristic cityscape at sunset" \
     --model-id "flux.1-dev" \
     --width 1024 --height 1024
   ```

2. The script automatically polls the job and prints asset IDs when done.

3. Download the generated images:
   ```bash
   python3 SKILL_DIR/scripts/download_asset.py --asset-id <asset_id> --output ./output/
   ```

**Supported generation modes** — use the `--mode` flag:

| Mode | Description | Extra Required Args |
|------|-------------|-------------------|
| `txt2img` | Text to image (default) | `--prompt`, `--model-id` |
| `img2img` | Image to image | `--prompt`, `--model-id`, `--image` |
| `controlnet` | ControlNet generation | `--prompt`, `--model-id`, `--image`, `--modality` |
| `inpaint` | Inpainting | `--prompt`, `--model-id`, `--image`, `--mask` |
| `upscale` | Image upscaling | `--image` |
| `remove-background` | Background removal | `--image` |
| `restyle` | Image restyling | `--prompt`, `--image` |
| `vectorize` | SVG vectorization | `--image` |

**Key parameters:**
- `--num-samples N` — number of images to generate (1-8, default 1)
- `--guidance N` — prompt adherence strength (default 7.5; Flux models use 3.5)
- `--steps N` — inference steps (5-50, default 30)
- `--seed N` — reproducible generation with fixed seed
- `--negative-prompt "..."` — what to avoid (Stable Diffusion only, not Flux)
- `--scheduler` — denoising scheduler (default: EulerAncestralDiscrete)

### 2. List & Search Assets

Find existing assets in the project:

```bash
# List recent assets
python3 SKILL_DIR/scripts/list_assets.py

# Filter by type
python3 SKILL_DIR/scripts/list_assets.py --type inference-txt2img

# Filter by model
python3 SKILL_DIR/scripts/list_assets.py --model-id <model_id>

# Search with multiple filters
python3 SKILL_DIR/scripts/list_assets.py \
  --type inference-txt2img \
  --sort-by createdAt --sort-direction desc \
  --page-size 20
```

Output is JSON with asset details including URLs, metadata, and generation parameters.

### 3. Download Assets

Download one or more assets to local filesystem:

```bash
# Single asset
python3 SKILL_DIR/scripts/download_asset.py --asset-id <id> --output ./downloads/

# Multiple assets
python3 SKILL_DIR/scripts/download_asset.py --asset-ids <id1> <id2> <id3> --output ./downloads/

# Download by inference (all images from one generation)
python3 SKILL_DIR/scripts/download_asset.py --inference-id <inference_id> --output ./downloads/
```

### 4. Check Job Status

Monitor any async operation:

```bash
python3 SKILL_DIR/scripts/poll_job.py --job-id <job_id>
```

The script polls every 3 seconds and prints final status with asset IDs on completion.

### 5. List Models

Browse available models:

```bash
# List your custom models
python3 SKILL_DIR/scripts/get_models.py

# List public models
python3 SKILL_DIR/scripts/get_models.py --public

# Filter by status
python3 SKILL_DIR/scripts/get_models.py --status trained
```

### 6. Direct API Calls

For advanced operations not covered by scripts, use `scenario_client.py` as a library:

```python
import subprocess, json, sys
sys.path.insert(0, "SKILL_DIR/scripts")
from scenario_client import ScenarioClient

client = ScenarioClient()

# Any GET request
response = client.get("/assets", params={"pageSize": "10"})

# Any POST request
response = client.post("/generate/txt2img", json={
    "prompt": "a cute robot",
    "modelId": "flux.1-dev",
    "width": 1024,
    "height": 1024
})
```

## Multi-Agent Usage

This skill is designed to work well with different agent types:

**Parallel generation** — spawn multiple agents to generate different images simultaneously:
- Each agent runs `generate.py` with different prompts
- All agents can poll their own jobs independently
- Collect all asset IDs at the end and batch download

**Research + Generate pattern:**
1. Use an Explore agent to find models: `get_models.py --public`
2. Use a general-purpose agent to generate with chosen model
3. Use another agent to download and organize results

**Batch pipeline:**
1. Agent 1: Generate N images with different seeds
2. Agent 2: List generated assets and filter by quality
3. Agent 3: Download selected assets and organize

## Common Model IDs

These public model IDs can be used directly without training:

| Model ID | Description |
|----------|-------------|
| `flux.1-dev` | Flux.1 Dev — high quality, guidance ~3.5 |
| `flux.1-schnell` | Flux.1 Schnell — fast generation |
| `sd-xl` | Stable Diffusion XL |

For custom models, use `get_models.py` to find your trained model IDs.

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 401 | Invalid credentials | Check SCENARIO_API_KEY and SCENARIO_API_SECRET |
| 403 | Insufficient permissions | Verify API key has required scopes |
| 404 | Resource not found | Check asset/model/job ID |
| 429 | Rate limited | Wait and retry (scripts handle this automatically) |
| 500 | Server error | Retry after a few seconds |

## Reference Documentation

For complete API endpoint details, parameter enums, and response schemas, read:
- `references/api_endpoints.md` — full endpoint catalog with parameters
- `references/generation_params.md` — detailed generation parameter reference

Read these reference files when you need specifics about a parameter's allowed values, response field meanings, or less common endpoints like collections, workflows, or model training.
