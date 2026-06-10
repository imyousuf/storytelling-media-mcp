from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


IMAGE_MODELS = {
    "flash": "gemini-3.1-flash-image",
    "pro": "gemini-3-pro-image",
    "legacy_flash": "gemini-2.5-flash-image",
}

DEFAULT_IMAGE_MODEL = IMAGE_MODELS["flash"]
DEFAULT_VIDEO_MODEL = "veo-3.1-generate-001"
PROJECT_ENV_VARS = ("GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_QUOTA_PROJECT", "GCLOUD_PROJECT")
LOCATION_ENV_VARS = ("GOOGLE_CLOUD_LOCATION", "GOOGLE_CLOUD_REGION", "GCLOUD_LOCATION")


class GoogleMediaError(RuntimeError):
    pass


class GoogleMediaClient:
    def __init__(
        self,
        api_key: str | None = None,
        auth_mode: str = "auto",
        user_project: str | None = None,
        location: str | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.auth_mode = auth_mode
        self.user_project = user_project or _first_env(PROJECT_ENV_VARS)
        self.location = location or _first_env(LOCATION_ENV_VARS) or "us-central1"
        if auth_mode not in {"auto", "api_key", "adc"}:
            raise GoogleMediaError("auth_mode must be one of: auto, api_key, adc.")
        if auth_mode == "api_key" and not self.api_key:
            raise GoogleMediaError("GEMINI_API_KEY or GOOGLE_API_KEY is required when auth_mode='api_key'.")

    def generate_image(
        self,
        *,
        prompt: str,
        output_path: Path,
        model: str = DEFAULT_IMAGE_MODEL,
        reference_image_paths: list[str] | None = None,
    ) -> dict[str, Any]:
        contents: list[Any] = [prompt]
        for image_path in reference_image_paths or []:
            contents.append(Image.open(image_path))

        response = self._client().models.generate_content(
            model=model,
            contents=contents,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        text: list[str] = []
        for part in response.parts or []:
            if part.text is not None:
                text.append(part.text)
                continue
            image = part.as_image()
            if image is not None:
                image.save(output_path)
                return {
                    "output_path": str(output_path),
                    "model": model,
                    "mime_type": _mime_type_for_output(output_path),
                    "text": text,
                }

        raise GoogleMediaError("No image was returned by the GenAI SDK response.")

    def generate_video(
        self,
        *,
        prompt: str,
        output_path: Path,
        model: str = DEFAULT_VIDEO_MODEL,
        aspect_ratio: str = "16:9",
        duration_seconds: int = 8,
        resolution: str = "720p",
        image_path: str | None = None,
        last_frame_path: str | None = None,
        reference_image_paths: list[str] | None = None,
        poll_interval_seconds: int = 10,
        timeout_seconds: int = 900,
    ) -> dict[str, Any]:
        client = self._client()
        image = Image.open(image_path) if image_path else None
        config_kwargs: dict[str, Any] = {
            "aspect_ratio": aspect_ratio,
            "duration_seconds": duration_seconds,
            "number_of_videos": 1,
            "resolution": resolution,
        }
        if last_frame_path:
            config_kwargs["last_frame"] = Image.open(last_frame_path)
        if reference_image_paths:
            config_kwargs["reference_images"] = [
                types.VideoGenerationReferenceImage(
                    image=Image.open(path),
                    reference_type="asset",
                )
                for path in reference_image_paths
            ]

        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(**config_kwargs),
        )

        deadline = time.monotonic() + timeout_seconds
        while not operation.done and time.monotonic() < deadline:
            time.sleep(poll_interval_seconds)
            operation = client.operations.get(operation)

        if not operation.done:
            raise GoogleMediaError(f"Timed out waiting for video operation: {operation.name}")
        if not operation.response or not operation.response.generated_videos:
            raise GoogleMediaError(f"No generated videos found in operation: {operation.name}")

        generated_video = operation.response.generated_videos[0]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(output_path))

        return {
            "output_path": str(output_path),
            "model": model,
            "operation": operation.name,
            "video_uri": getattr(generated_video.video, "uri", None),
        }

    def _client(self) -> genai.Client:
        if self.auth_mode in {"auto", "api_key"} and self.api_key:
            return genai.Client(api_key=self.api_key)

        if not self.user_project:
            raise GoogleMediaError(
                "GOOGLE_CLOUD_PROJECT is required when using auth_mode='adc'."
            )
        return genai.Client(
            vertexai=True,
            project=self.user_project,
            location=self.location,
        )


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _mime_type_for_output(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "image/png"
