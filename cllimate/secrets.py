import json
from os import environ
from pathlib import Path
from subprocess import run


def load_sops_secret(
    path: Path = Path(__file__).parent.parent / "conf" / "secrets" / "tokens.json",
):
    """Load the sops encrypted secrets file into the environment.

    Requires sops to be installed and configured.
    """
    text = run(
        f"sops -d {path.as_posix()}",
        check=True,
        shell=True,
        capture_output=True,
    ).stdout
    secrets = json.loads(text)
    for key, value in secrets.items():
        environ[key] = value
