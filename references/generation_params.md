# Generation Parameters Reference

## Common Parameters (all generation modes)

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| prompt | string | — | required | Text description of desired image |
| negativePrompt | string | — | "" | What to avoid (SD only, not Flux) |
| modelId | string | — | required | Model ID (public or custom) |
| numSamples | integer | 1-8 | 1 | Number of images to generate |
| guidance | number | — | 7.5 (SD) / 3.5 (Flux) | Prompt adherence strength |
| numInferenceSteps | integer | 5-50 | 30 | Denoising steps |
| width | integer | — | 512 | Image width in pixels |
| height | integer | — | 512 | Image height in pixels |
| seed | integer | — | random | Random seed for reproducibility |
| scheduler | string | — | EulerAncestralDiscrete | Denoising scheduler |

## Public Model IDs

| Model ID | Type | Recommended Guidance | Notes |
|----------|------|---------------------|-------|
| flux.1-dev | Flux | 3.5 | High quality, no negativePrompt |
| flux.1-schnell | Flux | 3.5 | Fast generation |
| sd-xl | SD-XL | 7.5 | Supports negativePrompt |

## Mode-Specific Parameters

### img2img
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Asset ID or data URL of input image |
| strength | number | How much to transform (0-1, flux-kontext) |

### controlnet
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Control image (asset ID or data URL) |
| modality | string | Control type: `canny`, `depth`, `grayscale`, `pose` |
| structureFidelity | number | 0-100, how closely to follow structure |

### inpaint
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Base image |
| mask | string | Mask image (white = inpaint area) |

### upscale
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Image to upscale |
| scalingFactor | number | 1-16, upscale multiplier |
| creativity | number | 0-100, creative freedom |

### restyle
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Image to restyle |
| prompt | string | Target style description |
| style | string | Preset: `anime`, `cartoon`, `cinematic`, `photo` |
| imageFidelity | number | 0-100, preserve original |
| promptFidelity | number | 0-100, follow prompt |

### remove-background
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Image for background removal |

### vectorize
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Image to convert to SVG |
| colorPrecision | number | Color detail level |
| pathPrecision | number | Path detail level |
| filterSpeckle | number | Noise filter |

### generative-fill
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Base image |
| mask | string | Area to fill |
| prompt | string | What to fill with |

### reframe
| Parameter | Type | Description |
|-----------|------|-------------|
| image | string | Image to extend |
| inputLocation | string | `top`, `bottom`, `left`, `right`, `middle` |
| targetWidth | number | 1024-16000 |
| targetHeight | number | 0-2048 |

### skybox
| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | string | Skybox description |
| geometryEnforcement | number | 0-100, horizon enforcement |

### texture
| Parameter | Type | Description |
|-----------|------|-------------|
| tileStyle | boolean | Seamless tiling |
| hdr | number | HDR intensity |

## Concepts (LoRA Composition)

Multiple LoRA models can be combined:

```json
{
  "concepts": [
    { "modelId": "model_A", "scale": 1.0 },
    { "modelId": "model_B", "scale": 0.5, "modelEpoch": "latest" }
  ]
}
```

- `scale`: -2 to 2, influence weight of each concept
- `modelEpoch`: optional, specific training epoch

## Asset Type Enum Values

Full list of `type` values for filtering:

**Generated:** `inference-txt2img`, `inference-img2img`, `inference-controlnet`, `inference-controlnet-img2img`, `inference-controlnet-inpaint`, `inference-controlnet-ip-adapter`, `inference-inpaint`, `inference-inpaint-ip-adapter`, `inference-txt2img-ip-adapter`, `inference-img2img-ip-adapter`, `inference-controlnet-reference`, `inference-reference`

**Textures:** `inference-txt2img-texture`, `inference-img2img-texture`, `inference-controlnet-texture`, `inference-reference-texture`, `texture`, `texture-albedo`, `texture-ao`, `texture-edge`, `texture-height`, `texture-metallic`, `texture-normal`, `texture-smoothness`

**3D:** `3d-texture`, `3d-texture-albedo`, `3d-texture-metallic`, `3d-texture-mtl`, `3d-texture-normal`, `3d-texture-roughness`, `3d23d`, `3d23d-texture`, `img23d`, `txt23d`, `uploaded-3d`

**Editing:** `background-removal`, `generative-fill`, `image-prompt-editing`, `patch`, `pixelization`, `reframe`, `restyle`, `segment`, `segmentation-image`, `segmentation-mask`, `upscale`, `vectorization`

**Media:** `img2video`, `txt2img`, `txt2video`, `video2img`, `video2video`, `txt2audio`, `audio2audio`, `uploaded-audio`, `uploaded-video`, `upscale-video`

**Skybox:** `skybox-base-360`, `skybox-3d`, `skybox-hdri`, `upscale-skybox`

**Other:** `canvas`, `canvas-drawing`, `canvas-export`, `detection`, `uploaded`, `uploaded-avatar`, `unknown`
