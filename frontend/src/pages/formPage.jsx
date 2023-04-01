import React, { useState } from "react";
import { Form, Col, OverlayTrigger, Tooltip } from "react-bootstrap";

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

  // IMPORTANT: ret len and call len must be smaller than or equal to instr len
  return (
    <Form
      id={"binaryInfoForm"}
      noValidate
      validated={validated}
      onSubmit={handleSubmit}
      className="row"
      style={{ width: "80%" }}
    >
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
    </Form>
  );
};

export default FormPage;
