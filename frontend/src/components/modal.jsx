import { Modal, Table } from "react-bootstrap";

const ModalInfo = ({ modalIsOpen, closeModal, activeModalNode, instructions }) => {
  if (activeModalNode != null)
    return (
      <Modal show={modalIsOpen} onHide={closeModal} centered size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Function {activeModalNode.f_id}</Modal.Title>
        </Modal.Header>
        <Modal.Body className="overflow-auto" style={{ maxHeight: "80vh" }}>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>#index</th>
                <th>hexa value</th>
                <th>...</th>
                <th>...</th>
              </tr>
            </thead>
            <tbody>
              {instructions.slice(activeModalNode.start, activeModalNode.end).map((e, i) => (
                <tr key={i}>
                  <td>{i + activeModalNode.start}</td>
                  <td>0x{("0000" + e.toString(16).toUpperCase()).slice(-4)}</td>
                  <td>...</td>
                  <td>...</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Modal.Body>
      </Modal>
    );
};

export default ModalInfo;
