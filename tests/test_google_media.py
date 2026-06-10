from storytelling_mcp.google_media import GoogleMediaClient


def test_client_reads_project_from_environment(monkeypatch):
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_QUOTA_PROJECT", raising=False)
    monkeypatch.delenv("GCLOUD_PROJECT", raising=False)
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "example-project-id")

    client = GoogleMediaClient(api_key="test-key")

    assert client.user_project == "example-project-id"
