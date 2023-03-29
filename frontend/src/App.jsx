import React, { useState } from "react";
import { Container, Row, Toast, ToastContainer } from "react-bootstrap";

import GraphPage from "./pages/graphPage";
import FormPage from "./pages/formPage";
import UploadPage from "./pages/uploadPage";
import IntroPage from "./pages/introPage";
import ProgressBar from "./components/progressBar";

import "./App.css";

const App = () => {
  const [graphData, setGraphData] = useState(null);
  const [formData, setFormData] = useState({
    instructionLength: null,
  });
  const [file, setFile] = useState(null);
  const [page, setPage] = useState(0);
  const [toastMessage, setToastMessage] = useState("");

  const postForm = async () => {
    var postFormData = new FormData();

    postFormData.append("data", JSON.stringify(formData));
    postFormData.append("file", file);

    return await fetch(
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
  };

  return (
    <Container fluid className="vh-100 d-flex flex-column">
      <Row>
        <ProgressBar page={page} />
      </Row>
      <Row className="flex-grow-1">
        {page == 0 && <IntroPage incPage={(x) => setPage(page + x)} />}
        {page == 1 && (
          <UploadPage
            setFile={setFile}
            file={file}
            incPage={(x) => setPage(page + x)}
            setToastMessage={setToastMessage}
          />
        )}
        {page == 2 && (
          <FormPage
            setFormData={setFormData}
            formData={formData}
            incPage={(x) => setPage(page + x)}
            postForm={postForm}
          />
        )}
        {page == 3 && graphData && (
          <GraphPage graphs={graphData} incPage={(x) => setPage(page + x)} />
        )}
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
