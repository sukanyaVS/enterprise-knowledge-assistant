import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_chroma_path_uses_dotenv_value():
    script = """
import os
import dotenv
from pathlib import Path

expected = Path(os.environ["EXPECTED_CHROMA_PATH"]).resolve()

def load_dotenv(*args, **kwargs):
    os.environ["CHROMA_PATH"] = os.environ["EXPECTED_CHROMA_PATH"]

dotenv.load_dotenv = load_dotenv

from backend.app.graph import nodes
from backend.app.retrieval import vector_store

assert nodes.CHROMA_PATH == expected
assert vector_store.CHROMA_PATH == expected
"""
    environment = os.environ.copy()
    environment.pop("CHROMA_PATH", None)
    environment["EXPECTED_CHROMA_PATH"] = str(
        PROJECT_ROOT / "test-chroma-config"
    )

    subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT_ROOT,
        env=environment,
        check=True,
    )
