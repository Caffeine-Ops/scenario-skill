# Scenario API Skill for Claude Code

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that provides CLI access to the [Scenario](https://scenario.com) platform for AI image generation, audio creation, asset management, and creative workflow automation.

## Features

- **Image Generation** — txt2img, img2img, ControlNet, inpainting, upscale, restyle, background removal, vectorization
- **Audio Generation** — text-to-audio via Gemini TTS (multiple voices and languages)
- **Asset Management** — list, search, filter, batch download project assets
- **Model Browsing** — discover public models and your custom-trained models
- **Multi-Agent** — designed for parallel generation and pipeline workflows
- **Zero Dependencies** — all scripts use Python standard library only

## Installation

### Option 1: Clone and register (recommended)

```bash
# Clone the repo
git clone git@github.com:Caffeine-Ops/scenario-skill.git

# Register as a Claude Code skill by adding to your project's .claude/settings.json
# or your global ~/.claude/settings.json:
```

Add to your Claude Code settings:

```json
{
  "skills": [
    "/path/to/scenario-skill"
  ]
}
```

### Option 2: Add as a project skill

Place the skill directory inside your project's `.claude/skills/` folder:

```bash
mkdir -p .claude/skills
cp -r /path/to/scenario-skill .claude/skills/scenario
```

### Option 3: Use the slash command

If you have the skill installed, just type in Claude Code:

```
/scenario
```

## Configuration

### API Keys

Get your API credentials from the [Scenario dashboard](https://app.scenario.com/settings/api):

```bash
# Add to your ~/.zshrc or ~/.bashrc
export SCENARIO_API_KEY="your_api_key"
export SCENARIO_API_SECRET="your_api_secret"
```

Reload your shell:

```bash
source ~/.zshrc
```

## Usage

Once the skill is installed, just ask Claude Code in natural language:

### Generate Images

```
> Generate a cute pixel art robot using flux.1-dev at 1024x1024
> Create 4 variations of a fantasy landscape with sd-xl
> Remove the background from ./photo.png and upscale it 4x
```

### Audio

```
> Generate a chess game sound effect with pieces clacking on wood
> Create a narration audio clip saying "Welcome to the game"
```

### Manage Assets

```
> Show me all images I generated this week
> Download the last 10 generated assets to ./output/
> List all public models with 3D tags
```

### Advanced Pipelines

```
> Generate 3 character designs, remove their backgrounds, then upscale all to 2048px
> Find all my txt2img assets from the last month and batch download them
```

Claude Code will automatically use the appropriate scripts and handle the async job polling.

## Project Structure

```
scenario-skill/
├── SKILL.md                  # Skill instructions (loaded by Claude Code)
├── scripts/
│   ├── scenario_client.py    # Core API client (auth, requests, polling)
│   ├── generate.py           # Image generation (12 modes)
│   ├── list_assets.py        # Asset listing with full filter support
│   ├── download_asset.py     # Download assets to local filesystem
│   ├── poll_job.py           # Poll async job status
│   └── get_models.py         # Browse available models
├── references/
│   ├── api_endpoints.md      # Complete API endpoint reference (80+ endpoints)
│   └── generation_params.md  # Generation parameter details
└── evals/
    └── evals.json            # Test cases
```

## Scripts Reference

All scripts are standalone CLI tools. They read `SCENARIO_API_KEY` and `SCENARIO_API_SECRET` from environment variables.

### generate.py

```bash
python3 scripts/generate.py \
  --mode txt2img \
  --prompt "a futuristic city" \
  --model-id flux.1-dev \
  --width 1024 --height 1024 \
  --num-samples 2 \
  --download ./output/
```

**Modes:** `txt2img`, `img2img`, `controlnet`, `inpaint`, `upscale`, `remove-background`, `restyle`, `vectorize`, `generative-fill`, `reframe`, `pixelate`, `segment`

### list_assets.py

```bash
python3 scripts/list_assets.py \
  --type inference-txt2img \
  --sort-by createdAt --sort-direction desc \
  --page-size 20 \
  --summary
```

### download_asset.py

```bash
# Single asset
python3 scripts/download_asset.py --asset-id <id> -o ./downloads/

# Multiple assets
python3 scripts/download_asset.py --asset-ids <id1> <id2> -o ./downloads/

# All assets from one generation
python3 scripts/download_asset.py --inference-id <id> -o ./downloads/
```

### get_models.py

```bash
python3 scripts/get_models.py --public --summary
```

## Common Model IDs

| Model ID | Type | Best For |
|----------|------|----------|
| `flux.1-dev` | Flux | High quality images (guidance ~3.5) |
| `flux.1-schnell` | Flux | Fast generation |
| `sd-xl` | SD-XL | Supports negative prompts |
| `model_google-gemini-2-5-flash-tts` | TTS | Audio generation |
| `model_jPeYYXRp175rcyoxXaGXX1rm` | LoRA | Sleek 3D-style assets |
| `model_t6bwwA6Qaj2gZywy8FrpxEdJ` | LoRA | Juicy game icons |

Use `get_models.py --public --summary` to discover more.

## License

MIT
