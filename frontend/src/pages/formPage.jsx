import React from "react";
import { Form, Col, Row, OverlayTrigger, Tooltip, InputGroup } from "react-bootstrap";

import useForm from "../hooks/useForm";

const FormPage = () => {
  const { formData, setFormElement, formValidated } = useForm();

  return (
    <Form id={"binaryInfoForm"} noValidate validated={formValidated} style={{ width: "80%" }}>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupInstrLength">
            <Form.Label>Instruction Length&nbsp;</Form.Label>
            <OverlayTrigger placement={"right"} overlay={<Tooltip>Length of instruction in bits</Tooltip>}>
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={64}
              required
              placeholder="Ex. 16"
              value={formData.instructionLength ?? ""}
              onChange={(e) => setFormElement("instructionLength", e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupEndiannes">
            <Form.Label>Endiannes&nbsp;</Form.Label>
            <OverlayTrigger placement={"right"} overlay={<Tooltip>Big vs little endiannes</Tooltip>}>
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control as="select" required onChange={(e) => setFormElement("endiannes", e.target.value)}>
              <option value="big">Big</option>
              <option value="little">Little</option>
            </Form.Control>
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupRetOpcodeLength">
            <Form.Label>Ret opcode Length&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Length of the opcode of the return instruction in bits</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={formData.instructionLength ?? 64}
              required
              value={formData.retOpcodeLength ?? ""}
              placeholder="Ex. 16"
              onChange={(e) => setFormElement("retOpcodeLength", e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupCallOpcodeLength">
            <Form.Label>Call opcode Length&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Length of the opcode of the call instruction in bits</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={formData.instructionLength ?? 64}
              required
              value={formData.callOpcodeLength ?? ""}
              placeholder="Ex. 4"
              onChange={(e) => setFormElement("callOpcodeLength", e.target.value)}
            />
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupFileOffset">
            <Form.Label>File offset start&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Byte position of where in the file the code section starts</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <InputGroup>
              <InputGroup.Text>0x</InputGroup.Text>
              <Form.Control
                required
                value={
                  formData.fileOffset
                    ? formData.fileOffset.toString(16).toUpperCase()
                    : formData.fileOffset === 0
                    ? 0
                    : ""
                }
                placeholder="Ex. 0"
                onChange={(e) => {
                  const input = e.currentTarget.value;
                  if (/^[0-9A-Fa-f]+$/.test(e.currentTarget.value) || input === "") {
                    setFormElement("fileOffset", parseInt(e.target.value, 16));
                  }
                }}
              />
            </InputGroup>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupFileOffsetEnd">
            <Form.Label>File offset end&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Byte position of where in the file the code section ends</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <InputGroup>
              <InputGroup.Text>0x</InputGroup.Text>
              <Form.Control
                required
                value={
                  formData.fileOffsetEnd
                    ? formData.fileOffsetEnd.toString(16).toUpperCase()
                    : formData.fileOffsetEnd === 0
                    ? 0
                    : ""
                }
                placeholder="Ex. 430"
                onChange={(e) => {
                  if (/^[0-9A-Fa-f]+$/.test(e.currentTarget.value) || e.currentTarget.value === "") {
                    setFormElement("fileOffsetEnd", parseInt(e.target.value, 16));
                  }
                }}
              />
            </InputGroup>
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupPcOffset">
            <Form.Label>PC offset&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>The byte position in hexadecimal of the first instruction in virtual memory</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <InputGroup>
              <InputGroup.Text>0x</InputGroup.Text>
              <Form.Control
                required
                value={
                  formData.pcOffset ? formData.pcOffset.toString(16).toUpperCase() : formData.pcOffset === 0 ? 0 : ""
                }
                placeholder="Ex. 200"
                onChange={(e) => {
                  const input = e.currentTarget.value;
                  if (/^[0-9A-Fa-f]+$/.test(e.currentTarget.value) || input === "") {
                    setFormElement("pcOffset", parseInt(e.target.value, 16));
                  }
                }}
              />
            </InputGroup>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupPcIncerPerInstruction">
            <Form.Label>PC increments&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  How many bits the instruction pointer increase between each instruction (usually same as instruction
                  length in bytes, i.e 16 bit instruction then increment pc by 2 )
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={16}
              required
              value={formData.pcIncPerInstr ?? ""}
              placeholder="Ex. 2"
              onChange={(e) => setFormElement("pcIncPerInstr", e.target.value)}
            />
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupCallCandidateRange">
            <Form.Label>Call candidate range&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  When searching for call candidates, we do a frequency analysis. If you choose for example 0 and 5 for
                  this range, only the 5 most frequent instructions will be evaluated as a possible call candidate, this
                  lets you reduce the search space and improve accuracy
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <InputGroup>
              <Form.Control
                type="number"
                min={0}
                max={64}
                required
                value={formData.callCandidateRange[0] ?? ""}
                placeholder="Ex. 3"
                onChange={(e) => setFormElement("callCandidateRange", [e.target.value, formData.callCandidateRange[1]])}
              />
              <Form.Control
                type="number"
                min={0}
                max={64}
                required
                value={formData.callCandidateRange[1] ?? ""}
                placeholder="Ex. 7"
                onChange={(e) => setFormElement("callCandidateRange", [formData.callCandidateRange[0], e.target.value])}
              />
            </InputGroup>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupRetCandidateRange">
            <Form.Label>Ret candidate range&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  When searching for return candidates, we do a frequency analysis. If you choose for example 0 and 5
                  for this range, only the 5 most frequent instructions will be evaluated as a possible return
                  candidate, this lets you reduce the search space and improve accuracy
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <InputGroup>
              <Form.Control
                type="number"
                min={0}
                max={64}
                required
                value={formData.retCandidateRange[0] ?? ""}
                placeholder="Ex. 0"
                onChange={(e) => setFormElement("retCandidateRange", [e.target.value, formData.retCandidateRange[1]])}
              />
              <Form.Control
                type="number"
                min={0}
                max={64}
                required
                value={formData.retCandidateRange[1] ?? ""}
                placeholder="Ex. 10"
                onChange={(e) => setFormElement("retCandidateRange", [formData.retCandidateRange[0], e.target.value])}
              />
            </InputGroup>
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupReturnToFunctionPrologueDistance">
            <Form.Label>Ret and prologue distance&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  The amount of instruction between a return instruction, and the prologue of the following function, we
                  search the whole space up to and including this value.
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={16}
              required
              value={formData.returnToFunctionPrologueDistance ?? ""}
              placeholder="Ex. 4"
              onChange={(e) => setFormElement("returnToFunctionPrologueDistance", e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupNrCandidates">
            <Form.Label>Number of Candidates&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  This option lets you choose the amount of candidate graphs to display on the next page
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={1}
              max={64}
              required
              value={formData.nrCandidates ?? ""}
              placeholder="Ex. 4"
              onChange={(e) => setFormElement("nrCandidates", e.target.value)}
            />
          </Form.Group>
        </Col>
      </Row>
    </Form>
  );
};

export default FormPage;
