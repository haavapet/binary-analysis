import React from "react";
import { Button, Col } from "react-bootstrap";

const GraphButton = ({ onClick, left, right, disabled }) => {
  if (left)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button className="btn-secondary" onClick={onClick} disabled={disabled}>
          {String.fromCharCode(8592)}
        </Button>
      </Col>
    );
  if (right)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button className="btn-secondary" onClick={onClick} disabled={disabled}>
          {String.fromCharCode(8594)}
        </Button>
      </Col>
    );
};

export default GraphButton;
