import React, { useState } from "react";
import { Row } from "react-bootstrap";

import Graph from "../components/graph";
import ModalInfo from "../components/modal";
import PageButton from "../components/button";

import "./graphPage.css";

const GraphPage = ({ graphs }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [activeModalNode, setActiveModalNode] = useState(null);
  const [selectedGraph, setSelectedGraph] = useState(0);

  function openModal(node) {
    setActiveModalNode(node);
    setModalIsOpen(true);
  }

  function closeModal() {
    setModalIsOpen(false);
    setActiveModalNode(null);
  }

  return (
    <>
      <ModalInfo
        modalIsOpen={modalIsOpen}
        closeModal={closeModal}
        activeModalNode={activeModalNode}
        instructions={graphs.instructions}
      />

      <Row style={{ textAlign: "center" }}>
        <h2>Graph {selectedGraph + 1}</h2>
      </Row>
      <Row style={{ height: "80%", backgroundColor: "#ddd", width: "80%" }}>
        <Graph
          graph={graphs.cfgs[selectedGraph]?.graph}
          openModal={openModal}
        />
      </Row>
      <Row style={{ marginTop: "20px", textAlign: "center" }}>
        <PageButton
          left
          onClick={() => setSelectedGraph(selectedGraph - 1)}
          disabled={selectedGraph === 0}
        />
        <PageButton
          right
          onClick={() => setSelectedGraph(selectedGraph + 1)}
          disabled={selectedGraph === graphs.cfgs.length - 1}
        />
      </Row>
    </>
  );
};

export default GraphPage;
