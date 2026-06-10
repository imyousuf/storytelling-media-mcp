# Storytelling Media MCP

MCP tools for an agent-driven video creation workflow.

This server gives Codex, Claude Code, or another MCP client access to:

- Nano Banana image generation and editing through Google's GenAI SDK.
- Veo 3.1 video generation through Google's GenAI SDK.
- Local video stitching through FFmpeg.

## Models

Image generation defaults to the newer Google image models:

- `flash`: `gemini-3.1-flash-image` also described by Google as Nano Banana 2.
- `pro`: `gemini-3-pro-image` also described by Google as Nano Banana Pro.
- `legacy_flash`: `gemini-2.5-flash-image` for older Nano Banana workflows.

Video generation defaults to:

- `veo-3.1-generate-001`

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
cp .env.template .env
```

FFmpeg must be installed and available on `PATH` for stitching.

### ADC Instead of API Key

The Gemini API can also use OAuth/ADC, but the ADC login must include Google's Gemini scope:

```bash
gcloud auth application-default login \
  --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
```

Then run the MCP server with `GOOGLE_CLOUD_PROJECT` set to the project that should be used for quota and billing:

```bash
python -m storytelling_mcp
```

The server also accepts `GOOGLE_CLOUD_QUOTA_PROJECT` or `GCLOUD_PROJECT`. Then call the image or video tools with `auth_mode="adc"`. If your ADC token was created without the `generative-language.retriever` scope, the Gemini API returns `ACCESS_TOKEN_SCOPE_INSUFFICIENT`.

## Run

```bash
python -m storytelling_mcp
```

## MCP Client Config

Example stdio server config using an API key:

```json
{
  "mcpServers": {
    "storytelling-media": {
      "command": "python",
      "args": ["-m", "storytelling_mcp"],
      "env": {
        "GEMINI_API_KEY": "your_api_key"
      }
    }
  }
}
```

Example stdio server config using ADC/Vertex:

```json
{
  "mcpServers": {
    "storytelling-media": {
      "command": "python",
      "args": ["-m", "storytelling_mcp"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-gcp-project-id",
        "GOOGLE_CLOUD_LOCATION": "us-central1"
      }
    }
  }
}
```

## Agent Plugins

This repo includes installable plugin metadata for both Claude Code and Codex.

Claude Code:

```text
/plugin marketplace add imyousuf/storytelling-media-mcp
/plugin install storytelling-media-mcp@storytelling-media
```

Codex:

```bash
codex plugin marketplace add imyousuf/storytelling-media-mcp --sparse .agents/plugins --sparse plugins
```

Then open `/plugins` in Codex and install `storytelling-media-mcp` from the `storytelling-media` marketplace.

The plugin launcher uses `STORYTELLING_MEDIA_MCP_ROOT` for local development. If that variable is unset, it creates a plugin-local virtual environment and installs this package from GitHub before starting the MCP server.

## Tools

- `nano_banana_generate_image`: text-to-image or text-and-image-to-image.
- `veo_generate_video`: text-to-video, image-to-video, interpolation, or reference-image-guided generation.
- `stitch_videos`: concatenate local MP4 clips with FFmpeg.

Generated files are written to paths supplied by the caller.
