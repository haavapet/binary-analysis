import React from "react";
import { Button, Col } from "react-bootstrap";

const PageButton = ({ left, right, onClick, hidden, disabled }) => {
  if (left)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button className="btn-secondary" onClick={onClick} hidden={hidden}>
          {String.fromCharCode(8592)}
        </Button>
      </Col>
    );
  if (right)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button className="btn-secondary" onClick={onClick} disabled={disabled} hidden={hidden}>
          {String.fromCharCode(8594)}
        </Button>
      </Col>
    );
  return <Col></Col>;
};

export default PageButton;
