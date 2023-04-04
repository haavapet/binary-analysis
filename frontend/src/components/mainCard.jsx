import React from "react";
import { Col, Card } from "react-bootstrap";

import PageButton from "../components/button";

const MainCard = ({ children, page, file, setPage }) => {
  return (
    <>
      <PageButton left onClick={() => setPage(page - 1)} hidden={page == 0} />
      <Col xs={8} className="d-flex">
        <Card className="mx-auto">{children}</Card>
      </Col>
      {page == 2 ? (
        <PageButton right type={"submit"} form={"binaryInfoForm"} />
      ) : (
        <PageButton
          right
          onClick={() => setPage(page + 1)}
          disabled={page == 1 && file == null}
          hidden={page == 3}
        />
      )}
    </>
  );
};

export default MainCard;
