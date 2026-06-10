---
name: storytelling-media
description: Use the Storytelling Media MCP tools for Nano Banana image generation, Veo video generation, and FFmpeg video stitching.
---

Use this skill when the user asks to generate or edit images, generate videos, extend video clips, create video segments from reference images, or stitch generated clips together.

Prefer the plugin-provided MCP tools:

- `nano_banana_generate_image` for text-to-image and text-and-image-to-image generation.
- `veo_generate_video` for text-to-video, image-to-video, first/last-frame interpolation, and reference-image-guided video generation.
- `stitch_videos` for local FFmpeg concatenation.

Before using image or video generation, check whether the user wants API-key mode or ADC/Vertex mode if the auth mode is unclear. For ADC/Vertex usage, the environment should provide `GOOGLE_CLOUD_PROJECT` and usually `GOOGLE_CLOUD_LOCATION=us-central1`. For API-key usage, the environment should provide `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

Generated media should be written to explicit user-provided or project-local output paths. Avoid writing secrets into repository files.
