import React from "react";
import { Col, Card, Row } from "react-bootstrap";

import PageButton from "../components/button";

const IntroPage = ({ incPage }) => {
  return (
    <>
      <PageButton />
      <Col xs={8} className="d-flex">
        <Card className="mx-auto" style={{ color: "white", fontSize: "25px" }}>
          <Row>Welcome to binary analysis helper</Row>
          <Row>TODO more info here about what it does and how to use it</Row>
        </Card>
      </Col>
      <PageButton right onClick={() => incPage(1)} />
    </>
  );
};

export default IntroPage;
