import React from "react";
import { Button, Col } from "react-bootstrap";

const PageButton = ({ left, right, page, setPage, file }) => {
  if (page == 2 && right)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <input className="btn btn-secondary" type="submit" form="binaryInfoForm" value={String.fromCharCode(8594)} />
      </Col>
    );
  if (left)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button className="btn-secondary" onClick={() => setPage(page - 1)} hidden={page == 0}>
          {String.fromCharCode(8592)}
        </Button>
      </Col>
    );
  if (right)
    return (
      <Col className="d-flex justify-content-center align-items-center">
        <Button
          className="btn-secondary"
          onClick={() => setPage(page + 1)}
          disabled={page == 1 && file == null}
          hidden={page == 3}
        >
          {String.fromCharCode(8594)}
        </Button>
      </Col>
    );
  return <Col></Col>;
};

export default PageButton;
