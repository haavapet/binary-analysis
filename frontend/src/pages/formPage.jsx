import React, { useState } from "react";
import { Form, Col, Card } from "react-bootstrap";

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
        <Card className="mx-auto" style={{ borderRadius: "3%" }}>
          <Form
            id={"binaryInfoForm"}
            style={{ color: "white" }}
            noValidate
            validated={validated}
            onSubmit={handleSubmit}
          >
            <Form.Group className="mb-3" controlId="formGroupInstrLength">
              <Form.Label>Instruction Length</Form.Label>
              <Form.Control
                required
                type="number"
                placeholder="Enter instruction length"
                onChange={(e) =>
                  setFormData((prev) => {
                    return { ...prev, instructionLength: e.target.value };
                  })
                }
              />
            </Form.Group>
          </Form>
        </Card>
      </Col>
      <PageButton right type={"submit"} form={"binaryInfoForm"} />
    </>
  );
};

export default FormPage;
