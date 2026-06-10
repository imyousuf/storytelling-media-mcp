from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class StitchingError(RuntimeError):
    pass


def stitch_videos(
    *,
    input_paths: list[str],
    output_path: str,
    reencode: bool = False,
) -> dict[str, object]:
    if not input_paths:
        raise StitchingError("At least one input video is required.")

    inputs = [Path(path).resolve() for path in input_paths]
    missing = [str(path) for path in inputs if not path.exists()]
    if missing:
        raise StitchingError(f"Input videos do not exist: {missing}")

    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as concat_file:
        concat_path = Path(concat_file.name)
        for path in inputs:
            concat_file.write(f"file '{_escape_concat_path(path)}'\n")

    try:
        command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path)]
        if reencode:
            command += ["-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p"]
        else:
            command += ["-c", "copy"]
        command.append(str(output))

        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            raise StitchingError(completed.stderr.strip() or "ffmpeg failed")

        return {
            "output_path": str(output),
            "input_paths": [str(path) for path in inputs],
            "reencode": reencode,
            "command": command,
        }
    finally:
        concat_path.unlink(missing_ok=True)


def _escape_concat_path(path: Path) -> str:
    return str(path).replace("'", "'\\''")
