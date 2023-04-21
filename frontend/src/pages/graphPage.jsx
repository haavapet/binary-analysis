import React, { useState } from "react";
import { Row } from "react-bootstrap";

import useGraph from "../hooks/useGraph";
import Graph from "../components/graph";
import ModalInfo from "../components/modal";
import GraphButton from "../components/graphButton";

import "../styles/graphPage.css";

const GraphPage = () => {
  const { graphData } = useGraph();
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

  if (graphData)
    return (
      <>
        <ModalInfo
          modalIsOpen={modalIsOpen}
          closeModal={closeModal}
          activeModalNode={activeModalNode}
          instructions={graphData?.instructions}
        />
        <Row style={{ textAlign: "center" }}>
          <h2>Graph {selectedGraph + 1}</h2>
        </Row>
        <Row style={{ height: "80%", backgroundColor: "#ddd", width: "80%" }}>
          <Graph graph={graphData.cfgs[selectedGraph]?.graph} openModal={openModal} />
        </Row>
        <Row style={{ marginTop: "20px", textAlign: "center" }}>
          <GraphButton left onClick={() => setSelectedGraph(selectedGraph - 1)} disabled={selectedGraph === 0} />
          <GraphButton
            right
            onClick={() => setSelectedGraph(selectedGraph + 1)}
            disabled={selectedGraph === graphData.cfgs.length - 1}
          />
        </Row>
      </>
    );
};

export default GraphPage;
