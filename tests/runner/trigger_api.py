from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uuid
from pathlib import Path

app = FastAPI()
RUNS = {}

class RunRequest(BaseModel):
    suite: str = "smoke"

@app.get("/health")
def health():
    return {"status": "runner-up"}

@app.post("/run-tests")
def run_tests(req: RunRequest):
    run_id = str(uuid.uuid4())
    output_dir = Path("results") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    newman_cmd = [
        "newman", "run",
        "tests/postman/UserAPI.postman_collection.json",
        "-e", "tests/postman/env.json",
        "--reporters", "cli,json",
        "--reporter-json-export", str(output_dir / "newman-report.json")
    ]

    robot_cmd = [
        "robot",
        "-d", str(output_dir / "robot"),
        "tests/robot/suites"
    ]

    newman_result = subprocess.run(newman_cmd, capture_output=True, text=True)
    robot_result = subprocess.run(robot_cmd, capture_output=True, text=True)

    RUNS[run_id] = {
        "newman_rc": newman_result.returncode,
        "robot_rc": robot_result.returncode,
        "status": "PASS" if newman_result.returncode == 0 and robot_result.returncode == 0 else "FAIL",
        "result_path": str(output_dir)
    }
    return {"run_id": run_id, **RUNS[run_id]}

@app.get("/runs/{run_id}")
def get_run(run_id: str):
    return RUNS.get(run_id, {"status": "NOT_FOUND"})