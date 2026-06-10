from __future__ import annotations

import google.auth
import google.auth.transport.requests
from google import genai

from storytelling_mcp.google_media import PROJECT_ENV_VARS


def main() -> None:
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/generative-language.retriever",
        ]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    project = _project_from_env() or project
    print("adc: ok")
    print(f"project: {project or '<none>'}")
    print(f"credentials_type: {type(credentials).__name__}")

    try:
        client = genai.Client(vertexai=True, project=project, location="us-central1")
        models = [model.name for model in client.models.list()]
        print("genai_vertex_adc: ok")
        print(f"model_count: {len(models)}")
        print(f"image_models: {[model for model in models if 'image' in model][:10]}")
        print(f"veo_models: {[model for model in models if 'veo' in model][:10]}")
    except Exception as exc:
        print("genai_vertex_adc: failed")
        print(f"{type(exc).__name__}: {exc}")


def _project_from_env() -> str | None:
    import os

    for name in PROJECT_ENV_VARS:
        value = os.environ.get(name)
        if value:
            return value
    return None


if __name__ == "__main__":
    main()
