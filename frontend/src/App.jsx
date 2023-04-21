import React from "react";
import { Container, Row, Toast, ToastContainer, Col, Card } from "react-bootstrap";

import usePage from "./hooks/usePage";
import useToast from "./hooks/useToast";
import useForm from "./hooks/useForm";
import useApi from "./hooks/useApi";
import useGraph from "./hooks/useGraph";

import GraphPage from "./pages/graphPage";
import FormPage from "./pages/formPage";
import UploadPage from "./pages/uploadPage";
import IntroPage from "./pages/introPage";

import ProgressBar from "./components/progressBar";
import PageButton from "./components/pageButton";

import "./styles/App.css";

const App = () => {
  const { page, incrementPage, decrementPage } = usePage();
  const { toastMessage, setToastMessage } = useToast();
  const { formData, file, validateForm } = useForm();
  const { callApi } = useApi();
  const { setGraphData } = useGraph();

  const handleSubmit = async (event) => {
    if (validateForm(event)) {
      return await callApi(formData)
        .then((data) => setGraphData(data))
        .then(() => true)
        .catch((error) => setToastMessage("Network error: " + error));
    }
  };

  let onClickRight = async () => {
    if (page != 2 || (await handleSubmit())) incrementPage();
  };

  return (
    <Container fluid className="vh-100 d-flex flex-column">
      {/* Progress bar at the top of the page */}
      <Row>
        <ProgressBar />
      </Row>

      {/* The main card which displays the different pages/steps */}
      <Row className="flex-grow-1">
        <PageButton left onClick={decrementPage} hidden={page == 0} />
        <Col xs={8} className="d-flex">
          <Card className="mx-auto">
            {page == 0 && <IntroPage />}
            {page == 1 && <UploadPage />}
            {page == 2 && <FormPage handleSubmit={handleSubmit} />}
            {page == 3 && <GraphPage />}
          </Card>
        </Col>
        <PageButton right onClick={onClickRight} hidden={page == 3} disabled={page == 1 && file == null} />
      </Row>

      {/* Below is for error message, and is rarely visible */}
      <ToastContainer className="p-3 position-fixed" position="bottom-center">
        <Toast onClose={() => setToastMessage("")} show={toastMessage != ""} delay={5000} autohide>
          <Toast.Body>{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
};

export default App;
