from pathlib import Path

from storytelling_mcp.google_media import (
    GoogleMediaClient,
    _image_api_version_for_model,
    _image_location_for_model,
    _mime_type_for_input,
)


def test_client_reads_project_from_environment(monkeypatch):
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_QUOTA_PROJECT", raising=False)
    monkeypatch.delenv("GCLOUD_PROJECT", raising=False)
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "example-project-id")

    client = GoogleMediaClient(api_key="test-key")

    assert client.user_project == "example-project-id"


def test_gemini_31_flash_image_uses_vertex_global_endpoint():
    assert _image_location_for_model("gemini-3.1-flash-image", "us-central1") == "global"
    assert _image_api_version_for_model("gemini-3.1-flash-image") == "v1"


def test_legacy_image_model_keeps_configured_location():
    assert _image_location_for_model("gemini-2.5-flash-image", "us-central1") == "us-central1"
    assert _image_api_version_for_model("gemini-2.5-flash-image") is None


def test_image_input_mime_type_from_suffix():
    assert _mime_type_for_input(Path("reference.jpg")) == "image/jpeg"
    assert _mime_type_for_input(Path("reference.webp")) == "image/webp"
    assert _mime_type_for_input(Path("reference.png")) == "image/png"
