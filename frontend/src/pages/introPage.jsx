import React from "react";
import { Row } from "react-bootstrap";

const IntroPage = () => {
  return (
    <>
      <Row>
        <h1>Welcome to binary analysis tool</h1>
      </Row>
      <Row style={{ width: "70%", paddingTop: "40px" }}>
        This tool will assist you in reverse engineering a binary from an unknown instruction set architecture. Click
        the arrow button on the right to start. You will first be asked to input a binary file, and then some
        information about the ISA. This can either be known, or you can guesstimate and test different configurations.
        The last page will display a function call graph of the analysed binary, you can click the nodes/functions to
        view the corresponding instructions.
      </Row>
    </>
  );
};

export default IntroPage;
