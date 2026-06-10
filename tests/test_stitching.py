from pathlib import Path

from storytelling_mcp import stitching


def test_stitch_videos_builds_ffmpeg_command(tmp_path, monkeypatch):
    first = tmp_path / "first.mp4"
    second = tmp_path / "second.mp4"
    output = tmp_path / "final.mp4"
    first.write_bytes(b"first")
    second.write_bytes(b"second")

    def fake_run(command, text, capture_output, check):
        Path(command[-1]).write_bytes(b"stitched")

        class Completed:
            returncode = 0
            stderr = ""

        return Completed()

    monkeypatch.setattr(stitching.subprocess, "run", fake_run)

    result = stitching.stitch_videos(
        input_paths=[str(first), str(second)],
        output_path=str(output),
    )

    assert result["output_path"] == str(output.resolve())
    assert result["command"][-2:] == ["copy", str(output.resolve())]
    assert output.read_bytes() == b"stitched"
