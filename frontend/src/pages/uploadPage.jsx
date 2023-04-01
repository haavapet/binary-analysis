import React from "react";
import { Col, Card } from "react-bootstrap";

import UploadFile from "../components/uploadFile";
import PageButton from "../components/button";

import "./uploadPage.css";

const UploadPage = ({ setFile, file, incPage, setToastMessage }) => {
  return (
    <>
      <PageButton left onClick={() => incPage(-1)} />
      <Col xs={8} className="d-flex">
        <Card className="mx-auto">
          <UploadFile
            setFile={setFile}
            file={file}
            setToastMessage={setToastMessage}
          />
        </Card>
      </Col>
      <PageButton right onClick={() => incPage(1)} disabled={file == null} />
    </>
  );
};

export default UploadPage;
