import React from "react";
import { Button, Col } from "react-bootstrap";

const PageButton = ({ onClick, left, right, disabled, type, form, hidden }) => {
  if (type == "submit")
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <input
          className="btn btn-secondary"
          disabled={disabled}
          type={type}
          form={form}
          value={String.fromCharCode(8594)}
        ></input>
      </Col>
    );
  if (left)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button
          className="btn-secondary"
          onClick={onClick}
          disabled={disabled}
          hidden={hidden}
        >
          {String.fromCharCode(8592)}
        </Button>
      </Col>
    );
  if (right)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button
          className="btn-secondary"
          onClick={onClick}
          disabled={disabled}
          hidden={hidden}
        >
          {String.fromCharCode(8594)}
        </Button>
      </Col>
    );
  return <Col></Col>;
};

export default PageButton;
