# this script can be used to pack and upload a python .pex file to an gcs bucket
# requires docker and gsutil

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

REQUIREMENTS_TXT = SCRIPT_DIR / "requirements.txt"
DAGSTER_DIR = (
    Path(*SCRIPT_DIR.parts[: SCRIPT_DIR.parts.index("dagster-io")])
    / "dagster-io/dagster"
)

parser = argparse.ArgumentParser(description="Build & upload a PEX executable to GCS")
parser.add_argument(
    "--gcs-dir",
    type=str,
    help="gcs directory to copy files into",
)


def main():
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        env = {**os.environ, "DOCKER_BUILDKIT": "1"}
        subprocess.run(
            [
                "docker",
                "build",
                "--output",
                "type=local,dest=./output",
                "-f",
                str(SCRIPT_DIR / "dev.Dockerfile"),
                str(DAGSTER_DIR),
            ],
            env=env,
            shell=False,
            check=True,
        )
        subprocess.run(
            ["gsutil", "cp", "./output/venv.pex", os.path.join(args.gcs_dir, "venv.pex")],
            shell=False,
            check=True,
        )
        subprocess.run(
            [
                "gsutil",
                "cp",
                str(SCRIPT_DIR / "script.py"),
                os.path.join(args.gcs_dir, "script.py"),
            ],
            shell=False,
            check=True,
        )


if __name__ == "__main__":
    main()
