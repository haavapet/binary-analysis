import React, { useState } from "react";
import { Container, Row, Toast, ToastContainer, Col, Card } from "react-bootstrap";

import GraphPage from "./pages/graphPage";
import FormPage from "./pages/formPage";
import UploadPage from "./pages/uploadPage";
import IntroPage from "./pages/introPage";
import ProgressBar from "./components/progressBar";

import "./App.css";
import PageButton from "./components/pageButton";

const App = () => {
  const [graphData, setGraphData] = useState(null);
  const [formData, setFormData] = useState({
    instructionLength: null,
    endiannes: "big",
    retOpcodeLength: null,
    callOpcodeLength: null,
    fileOffset: null,
    fileOffsetEnd: null,
    pcOffset: null,
    pcIncPerInstr: null,
    callCandidateRange: [null, null],
    retCandidateRange: [null, null],
    returnToFunctionPrologueDistance: null,
    nrCandidates: null,
  });
  const [file, setFile] = useState(null);
  const [page, setPage] = useState(0);
  const [toastMessage, setToastMessage] = useState("");

  const postForm = async () => {
    var postFormData = new FormData();

    postFormData.append("file", file);
    for (const name in formData) {
      // Arrays/lists needs to be encoded with key,value for each item in the array
      if (formData[name] instanceof Array) {
        postFormData.append(name, formData[name][0]);
        postFormData.append(name, formData[name][1]);
      } else {
        postFormData.append(name, formData[name]);
      }
    }

    let result = await fetch(`http://${process.env.REACT_APP_BACKEND_URL || "localhost:8000"}/api`, {
      method: "POST",
      body: postFormData,
    })
      .then((response) => response.json())
      .then((data) => {
        setGraphData(data);
        return true;
      })
      .catch((error) => {
        setToastMessage("Network error: " + error);
        return false;
      });

    if (result) setPage(page + 1);
  };

  return (
    <Container fluid className="vh-100 d-flex flex-column">
      {/* Progress bar at the top of the page */}
      <Row>
        <ProgressBar page={page} />
      </Row>

      {/* The main card which displays the different pages/steps */}
      <Row className="flex-grow-1">
        <PageButton left page={page} setPage={setPage} />
        <Col xs={8} className="d-flex">
          <Card className="mx-auto">
            {page == 0 && <IntroPage />}
            {page == 1 && <UploadPage setFile={setFile} file={file} setToastMessage={setToastMessage} />}
            {page == 2 && <FormPage setFormData={setFormData} formData={formData} postForm={postForm} />}
            {page == 3 && graphData && <GraphPage graphs={graphData} />}
          </Card>
        </Col>
        <PageButton right page={page} setPage={setPage} file={file} />
      </Row>

      {/* Below is for error message, and is rarely visible */}
      <ToastContainer className="p-3" position="bottom-center">
        <Toast onClose={() => setToastMessage("")} show={toastMessage != ""} delay={5000} autohide>
          <Toast.Body>{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
};

export default App;
