import subprocess
from pathlib import Path

subprocess.check_call(
    "python -m sphinx -T -E -b html -d _build/doctrees -D language=en . html",
    cwd=Path(__file__).parent)
