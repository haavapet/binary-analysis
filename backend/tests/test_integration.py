import json

from fastapi.testclient import TestClient

from ..app.controller import app

client = TestClient(app)

def test_integration() -> None:

    data={
            "instructionLength": "16",
            "endiannes": "big",
            "retOpcodeLength": "16",
            "callOpcodeLength": "4",
            "fileOffset": "0",
            "fileOffsetEnd": str(0x430),
            "pcOffset": str(0x200),
            "pcIncPerInstr": "2",
            "callCandidateRange": ["3", "7"],
            "retCandidateRange":["0", "10"],
            "returnToFunctionPrologueDistance": "4",
            "nrCandidates": "1",
            "unknownCodeEntry": "False",
            "includeInstructions": "False",
            "isRelativeAddressing": "False",
        }

    filename = '../binaries/chipquarium.ch8'
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

    top_graph = json.loads(res.content)["cfgs"][0]

    assert top_graph["probability"] > 0.9

    assert top_graph["call_opcode"] == 0x2000

    assert top_graph["ret_opcode"] == 0x00EE
