# MCP Client Configuration

## Codex

Add a stdio MCP server entry to your Codex MCP configuration. For API key usage:

```json
{
  "mcpServers": {
    "storytelling-media": {
      "command": "python",
      "args": ["-m", "storytelling_mcp"],
      "cwd": "/media/files/projects/storytelling",
      "env": {
        "GEMINI_API_KEY": "your_api_key",
        "GOOGLE_CLOUD_PROJECT": "your-gcp-project-id",
        "GOOGLE_CLOUD_LOCATION": "us-central1"
      }
    }
  }
}
```

For ADC/Vertex usage:

```json
{
  "mcpServers": {
    "storytelling-media": {
      "command": "python",
      "args": ["-m", "storytelling_mcp"],
      "cwd": "/media/files/projects/storytelling",
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-gcp-project-id",
        "GOOGLE_CLOUD_LOCATION": "us-central1"
      }
    }
  }
}
```

## Claude Code

Use the same command, arguments, working directory, and environment variables in Claude Code's MCP server configuration.

## Plugin Installation

This repository also ships plugin marketplace metadata for both agents.

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

After installation, use `$movie-production-pipeline` for the staged director's-brief-to-production workflow, or use the MCP tools directly for image generation, video generation, and stitching.

## Notes

- The image and video tools call Google APIs through the GenAI SDK. Use either `GEMINI_API_KEY` or ADC/Vertex project env vars.
- For ADC/Vertex usage, the default Veo model is `veo-3.1-generate-001`.
- If you prefer ADC/OAuth, run:

```bash
gcloud auth application-default login \
  --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
```

Then pass `auth_mode="adc"` to the image or video tool. The server expects the GCP project ID from `GOOGLE_CLOUD_PROJECT`; it also accepts `GOOGLE_CLOUD_QUOTA_PROJECT` or `GCLOUD_PROJECT`.
- The stitching tool is local and requires `ffmpeg` on `PATH`.
- Generated media is written to the `output_path` provided by the agent.
