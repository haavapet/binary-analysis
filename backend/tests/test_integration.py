import json

from fastapi.testclient import TestClient

from ..app.controller import app

client = TestClient(app)
def test_integration() -> None:

    data={
            "instructionLength":16,
            "endiannes":"big",
            "retOpcodeLength":16,
            "callOpcodeLength":4,
            "fileOffset":0,
            "fileOffsetEnd": 0x430,
            "pcOffset":0x200,
            "pcIncPerInstr":2,
            "callCandidateRange": [3, 7],
            "retCandidateRange":[0,10],
            "returnToFunctionPrologueDistance":4,
            "nrCandidates":4,
        }

    filename = '../binaries/quar.ch8'
    with open(filename, "rb") as f:
        filebody = f.read()

    res = client.post(
        "/api",
        data=data,
        files={
            "file": ("quar.ch8", filebody),
        },
    )

    assert res.status_code == 200

    best_probability = json.loads(res.content)["cfgs"][0]["probability"]
    assert best_probability > 0.9
