import React, { useState } from "react";
import {
  Form,
  Col,
  Card,
  OverlayTrigger,
  Tooltip,
  FloatingLabel,
} from "react-bootstrap";

import PageButton from "../components/button";

const FormPage = ({ setFormData, formData, incPage, postForm }) => {
  const [validated, setValidated] = useState(false);

  async function handleSubmit(event) {
    const form = event.currentTarget;

    event.preventDefault();
    event.stopPropagation();

    if (form.checkValidity() === true && (await postForm()) === true) {
      incPage(1);
    }

    setValidated(true);
  }

  return (
    <>
      <PageButton left onClick={() => incPage(-1)} />
      <Col xs={8} className="d-flex">
        <Card className="mx-auto">
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
                <Form.Label style={{ color: "white" }}>
                  Instruction Length&nbsp;
                </Form.Label>
                <OverlayTrigger
                  placement={"right"}
                  overlay={<Tooltip>Length of instruction in bits</Tooltip>}
                >
                  <i
                    className="fa fa-question-circle"
                    style={{ color: "white" }}
                  />
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
                <Form.Label style={{ color: "white" }}>
                  Endiannes&nbsp;{" "}
                </Form.Label>
                <OverlayTrigger
                  placement={"right"}
                  overlay={<Tooltip>Big vs little endiannes</Tooltip>}
                >
                  <i
                    className="fa fa-question-circle"
                    style={{ color: "white" }}
                  />
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
                  <option value="">Choose endiannes</option>
                  <option value="big">Big</option>
                  <option value="little">Little</option>
                </Form.Control>
              </Form.Group>
            </Col>
          </Form>
        </Card>
      </Col>
      <PageButton right type={"submit"} form={"binaryInfoForm"} />
    </>
  );
};

export default FormPage;
