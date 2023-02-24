import subprocess
subprocess.check_call(
    "python -m sphinx -T -E -b html -d _build/doctrees -D language=en . html", shell=True)
