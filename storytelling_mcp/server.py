from __future__ import annotations

from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP

from storytelling_mcp.google_media import (
    DEFAULT_IMAGE_MODEL,
    DEFAULT_VIDEO_MODEL,
    IMAGE_MODELS,
    GoogleMediaClient,
)
from storytelling_mcp.stitching import stitch_videos as stitch_video_files


mcp = FastMCP("storytelling-media")


@mcp.tool()
def nano_banana_generate_image(
    prompt: str,
    output_path: str,
    model: Literal[
        "flash",
        "pro",
        "legacy_flash",
        "gemini-3.1-flash-image",
        "gemini-3-pro-image",
        "gemini-2.5-flash-image",
    ] = "flash",
    reference_image_paths: list[str] | None = None,
    auth_mode: Literal["auto", "api_key", "adc"] = "auto",
    user_project: str | None = None,
) -> dict[str, object]:
    """Generate or edit an image with Google's Nano Banana Gemini image models."""
    model_id = IMAGE_MODELS.get(model, model) or DEFAULT_IMAGE_MODEL
    return GoogleMediaClient(auth_mode=auth_mode, user_project=user_project).generate_image(
        prompt=prompt,
        output_path=Path(output_path),
        model=model_id,
        reference_image_paths=reference_image_paths,
    )


@mcp.tool()
def veo_generate_video(
    prompt: str,
    output_path: str,
    model: str = DEFAULT_VIDEO_MODEL,
    aspect_ratio: Literal["16:9", "9:16"] = "16:9",
    duration_seconds: Literal[4, 5, 6, 8] = 8,
    resolution: Literal["720p", "1080p", "4k"] = "720p",
    image_path: str | None = None,
    last_frame_path: str | None = None,
    reference_image_paths: list[str] | None = None,
    poll_interval_seconds: int = 10,
    timeout_seconds: int = 900,
    auth_mode: Literal["auto", "api_key", "adc"] = "auto",
    user_project: str | None = None,
) -> dict[str, object]:
    """Generate a video with Google's Veo 3.1 Gemini API."""
    if reference_image_paths and len(reference_image_paths) > 3:
        raise ValueError("Veo 3.1 supports up to three reference images.")
    if (reference_image_paths or resolution in {"1080p", "4k"}) and duration_seconds != 8:
        raise ValueError("Veo 3.1 requires duration_seconds=8 for reference images or 1080p/4k.")

    return GoogleMediaClient(auth_mode=auth_mode, user_project=user_project).generate_video(
        prompt=prompt,
        output_path=Path(output_path),
        model=model,
        aspect_ratio=aspect_ratio,
        duration_seconds=duration_seconds,
        resolution=resolution,
        image_path=image_path,
        last_frame_path=last_frame_path,
        reference_image_paths=reference_image_paths,
        poll_interval_seconds=poll_interval_seconds,
        timeout_seconds=timeout_seconds,
    )


@mcp.tool()
def stitch_videos(
    input_paths: list[str],
    output_path: str,
    reencode: bool = False,
) -> dict[str, object]:
    """Stitch local video files into one output file with FFmpeg."""
    return stitch_video_files(
        input_paths=input_paths,
        output_path=output_path,
        reencode=reencode,
    )


def main() -> None:
    mcp.run()
