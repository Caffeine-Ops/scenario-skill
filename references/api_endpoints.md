# Scenario API Endpoints Reference

Base URL: `https://api.cloud.scenario.com/v1`

## Assets

| Method | Path | Description |
|--------|------|-------------|
| GET | `/assets` | List project assets (supports filters, pagination, sorting) |
| POST | `/assets` | Upload image or canvas (base64 body) |
| DELETE | `/assets` | Batch delete (max 100 IDs) |
| POST | `/assets/download` | Request batch download link (max 1000) |
| GET | `/assets/download/{jobId}` | Get batch download status/URL |
| POST | `/assets/get-bulk` | Get multiple assets by IDs (max 200) |
| GET | `/assets/public` | List public assets |
| GET | `/assets/public/{assetId}` | Get specific public asset |
| GET | `/assets/{assetId}` | Get asset details |
| PUT | `/assets/{assetId}` | Update asset |
| POST | `/assets/{assetId}/copy` | Copy asset |
| PUT | `/assets/{assetId}/lock` | Lock asset |
| PUT | `/assets/{assetId}/unlock` | Unlock asset |
| PUT | `/assets/{assetId}/tags` | Update tags |
| GET | `/assets/{assetId}/snapshots` | Get canvas snapshots |
| POST | `/assets/{assetId}/download` | Download single asset |

### GET /assets Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| pageSize | string | Items per page (1-100, default 50) |
| paginationToken | string | Next page token |
| sortBy | string | `createdAt` or `updatedAt` |
| sortDirection | string | `asc` or `desc` |
| type | string | Single asset type filter |
| types | string[] | Multiple asset type filter |
| modelId | string | Filter by model |
| inferenceId | string | Filter by inference |
| authorId | string | Filter by creator |
| privacy | string | `private`, `public`, `unlisted` |
| parentAssetId | string | Children of parent |
| rootAssetId | string | Children of root |
| collectionId | string | Filter by collection |
| tags | string | Comma-separated (public only) |
| createdAfter | string | ISO date filter (needs sortBy=createdAt) |
| createdBefore | string | ISO date filter (needs sortBy=createdAt) |
| updatedAfter | string | ISO date filter (needs sortBy=updatedAt) |
| updatedBefore | string | ISO date filter (needs sortBy=updatedAt) |
| originalAssets | string | "true" for untransformed |

### Asset Object Schema

```json
{
  "id": "asset_xxx",
  "kind": "image|video|audio|3d|document|json|image-hdr",
  "status": "success|pending|error",
  "privacy": "private|public|unlisted",
  "url": "https://signed-url",
  "mimeType": "image/png",
  "ownerId": "proj_xxx",
  "authorId": "user_xxx",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "tags": [],
  "collectionIds": [],
  "editCapabilities": ["UPSCALE", "RESTYLE", ...],
  "metadata": { "type": "...", "prompt": "...", "modelId": "...", ... },
  "properties": { "size": 123, "width": 1024, "height": 1024 },
  "preview": { "assetId": "...", "url": "..." },
  "thumbnail": { "assetId": "...", "url": "..." },
  "nsfw": []
}
```

## Collections

| Method | Path | Description |
|--------|------|-------------|
| GET | `/collections` | List collections |
| POST | `/collections` | Create collection |
| GET | `/collections/{id}` | Get collection |
| PUT | `/collections/{id}` | Update collection |
| DELETE | `/collections/{id}` | Delete collection |
| PUT | `/collections/{id}/assets` | Add assets |
| DELETE | `/collections/{id}/assets` | Remove assets |
| PUT | `/collections/{id}/models` | Add models |
| DELETE | `/collections/{id}/models` | Remove models |

## Generation

### No Reference
| POST | `/generate/txt2img` | Text to image |

### Single Reference
| POST | `/generate/img2img` | Image to image |
| POST | `/generate/controlnet` | ControlNet |
| POST | `/generate/txt2img-ip-adapter` | Text + IP-Adapter |

### Dual Reference
| POST | `/generate/controlnet-img2img` | ControlNet + img2img |
| POST | `/generate/controlnet-ip-adapter` | ControlNet + IP-Adapter |
| POST | `/generate/img2img-ip-adapter` | img2img + IP-Adapter |

### Custom Models
| POST | `/generate/custom/{modelId}` | Generate with custom model |

### Image Editing
| POST | `/generate/patch` | Patch editing |
| POST | `/generate/pixelate` | Pixelation |
| POST | `/generate/prompt-editing` | Prompt-based editing |
| POST | `/generate/remove-background` | Background removal |
| POST | `/generate/vectorize` | SVG vectorization |

### Other Generation
| POST | `/generate/generative-fill` | Generative fill |
| POST | `/generate/inpaint` | Inpainting |
| POST | `/generate/controlnet-inpaint` | ControlNet inpainting |
| POST | `/generate/reframe` | Image reframing |
| POST | `/generate/restyle` | Image restyling |
| POST | `/generate/segment` | Image segmentation |
| POST | `/generate/upscale` | Image upscaling |
| POST | `/generate/skybox-base-360` | 360 skybox |
| POST | `/generate/skybox-upscale-360` | Skybox upscaling |
| POST | `/generate/detect` | Detection maps |
| POST | `/generate/embed` | Generate embeddings |

### Text Generation
| POST | `/generate/caption` | Generate captions |
| POST | `/generate/describe-style` | Describe image style |
| POST | `/generate/prompt` | Generate prompts |
| POST | `/generate/translate` | Translate text |

### Texture Generation
| POST | `/generate/texture` | Texture generation |
| POST | `/generate/txt2img-texture` | Text to texture |
| POST | `/generate/img2img-texture` | Image to texture |
| POST | `/generate/controlnet-texture` | ControlNet texture |

## Models

| Method | Path | Description |
|--------|------|-------------|
| GET | `/models` | List models |
| POST | `/models` | Create model |
| GET | `/models/{id}` | Get model details |
| PUT | `/models/{id}` | Update model |
| DELETE | `/models/{id}` | Delete model |
| POST | `/models/{id}/copy` | Copy model |
| POST | `/models/{id}/download` | Download model weights |
| POST | `/models/get-bulk` | Get multiple models |
| GET | `/models/public` | List public models |
| GET | `/models/public/{id}` | Get public model |

### Model Training
| PUT | `/models/{id}/train` | Configure training |
| POST | `/models/{id}/train/action` | Start/stop training |
| POST | `/models/{id}/training-images` | Upload training images |
| PUT | `/models/{id}/training-images/pairs` | Update training pairs |
| PUT | `/models/{id}/training-images/{imageId}` | Update training image |
| DELETE | `/models/{id}/training-images/{imageId}` | Delete training image |
| GET | `/models/{id}/scores/training-dataset` | Training dataset scores |

## Jobs

| Method | Path | Description |
|--------|------|-------------|
| GET | `/jobs` | List jobs |
| GET | `/jobs/{jobId}` | Get job details |
| POST | `/jobs/{jobId}/action` | Perform job action |

### Job Status Values
`pending` → `queued` → `warming-up` → `in-progress` → `finalizing` → `success`
Also: `failure`, `canceled`

## Other Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tags` | List tags |
| POST | `/uploads` | Upload files |
| GET | `/uploads/{id}` | Upload status |
| GET | `/usages` | Usage information |
| POST | `/search/assets` | Search assets |
| POST | `/search/models` | Search models |
| GET | `/recommendations/models` | Model recommendations |
| GET | `/oscu/prices` | Pricing info |

## Workflows

| Method | Path | Description |
|--------|------|-------------|
| GET | `/workflows` | List workflows |
| POST | `/workflows` | Create workflow |
| GET | `/workflows/{id}` | Get workflow |
| PUT | `/workflows/{id}` | Update workflow |
| DELETE | `/workflows/{id}` | Delete workflow |
| PUT | `/workflows/{id}/run` | Execute workflow |
| PUT | `/workflows/{id}/user-approval` | Approve workflow step |
| GET | `/workflows/tags` | Workflow tags |
