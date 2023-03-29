import { Col } from "react-bootstrap";

const ProgressBar = ({ page }) => {
  return (
    <Col
      className="d-flex justify-content-center align-items-center"
      style={{ paddingTop: "40px" }}
    >
      <div className={page == 0 ? "steps steps-active" : "steps"}>
        <img alt="" src={`${process.env.PUBLIC_URL}/img/info.jpeg`} />
      </div>

      <div className={page > 0 ? "line-active line" : "line"}>
        <div />
      </div>

      <div className={page == 1 ? "steps steps-active" : "steps"}>
        <img alt="" src={`${process.env.PUBLIC_URL}/img/upload.png`} />
      </div>

      <div className={page > 1 ? "line-active line" : "line"}>
        <div />
      </div>

      <div className={page == 2 ? "steps steps-active" : "steps"}>
        <img alt="" src={`${process.env.PUBLIC_URL}/img/form.png`} />
      </div>

      <div className={page > 2 ? "line-active line" : "line"}>
        <div />
      </div>

      <div className={page == 3 ? "steps steps-active" : "steps"}>
        <img alt="" src={`${process.env.PUBLIC_URL}/img/graph.jpg`} />
      </div>
    </Col>
  );
};

export default ProgressBar;
