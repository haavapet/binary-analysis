import React, { useState } from "react";
import { Container, Row, Toast, ToastContainer } from "react-bootstrap";

import GraphPage from "./pages/graphPage";
import FormPage from "./pages/formPage";
import UploadPage from "./pages/uploadPage";
import IntroPage from "./pages/introPage";
import ProgressBar from "./components/progressBar";
import MainCard from "./components/mainCard";

import "./App.css";

const App = () => {
  const [graphData, setGraphData] = useState(null);
  const [formData, setFormData] = useState({
    instructionLength: null,
    endiannes: "little",
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

    postFormData.append("data", JSON.stringify(formData));
    postFormData.append("file", file);

    let result = await fetch(
      `http://${process.env.REACT_APP_BACKEND_URL || "localhost:8000"}/api`,
      {
        method: "POST",
        body: postFormData,
      }
    )
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
      <Row>
        <ProgressBar page={page} />
      </Row>
      <Row className="flex-grow-1">
        <MainCard page={page} file={file} setPage={setPage}>
          {page == 0 && <IntroPage />}
          {page == 1 && (
            <UploadPage
              setFile={setFile}
              file={file}
              setToastMessage={setToastMessage}
            />
          )}
          {page == 2 && (
            <FormPage
              setFormData={setFormData}
              formData={formData}
              postForm={postForm}
            />
          )}
          {page == 3 && graphData && <GraphPage graphs={graphData} />}
        </MainCard>
      </Row>
      <ToastContainer className="p-3" position="bottom-center">
        <Toast
          onClose={() => setToastMessage("")}
          show={toastMessage != ""}
          delay={5000}
          autohide
        >
          <Toast.Body>{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
};

export default App;
