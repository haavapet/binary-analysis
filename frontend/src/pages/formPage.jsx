import React, { useState } from "react";
import { Form, Col, Row, OverlayTrigger, Tooltip } from "react-bootstrap";

const FormPage = ({ setFormData, formData, postForm }) => {
  const [validated, setValidated] = useState(false);

  async function handleSubmit(event) {
    const form = event.currentTarget;

    event.preventDefault();
    event.stopPropagation();

    if (form.checkValidity()) {
      await postForm();
    }

    setValidated(true);
  }

  return (
    <Form
      id={"binaryInfoForm"}
      noValidate
      validated={validated}
      onSubmit={handleSubmit}
      style={{ width: "80%" }}
    >
      <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupInstrLength">
            <Form.Label>Instruction Length&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Length of instruction in bits</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={64}
              required
              placeholder="Enter instruction length"
              value={formData.instructionLength ?? ""}
              onChange={(e) =>
                setFormData((prev) => {
                  return { ...prev, instructionLength: e.target.value };
                })
              }
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupEndiannes">
            <Form.Label>Endiannes&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={<Tooltip>Big vs little endiannes</Tooltip>}
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              as="select"
              required
              onSelect={(e) =>
                setFormData((prev) => {
                  return { ...prev, endiannes: e.target.value };
                })
              }
            >
              <option value="" hidden>
                Choose endiannes
              </option>
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
              overlay={
                <Tooltip>
                  Length of the opcode of the return instruction in bits
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={formData.instructionLength ?? 64}
              required
              value={formData.retOpcodeLength ?? ""}
              placeholder="Enter return opcode length"
              onChange={(e) =>
                setFormData((prev) => {
                  return { ...prev, retOpcodeLength: e.target.value };
                })
              }
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formGroupCallOpcodeLength">
            <Form.Label>Call opcode Length&nbsp;</Form.Label>
            <OverlayTrigger
              placement={"right"}
              overlay={
                <Tooltip>
                  Length of the opcode of the call instruction in bits
                </Tooltip>
              }
            >
              <i className="fa fa-question-circle" />
            </OverlayTrigger>
            <Form.Control
              type="number"
              min={0}
              max={formData.instructionLength ?? 64}
              required
              value={formData.callOpcodeLength ?? ""}
              placeholder="Enter call opcode length"
              onChange={(e) =>
                setFormData((prev) => {
                  return { ...prev, callOpcodeLength: e.target.value };
                })
              }
            />
          </Form.Group>
        </Col>
      </Row>
    </Form>
  );
};

export default FormPage;
