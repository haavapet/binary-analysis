import { Modal, Table } from "react-bootstrap";

import useForm from "../hooks/useForm";

const ModalInfo = ({ modalIsOpen, closeModal, activeModalNode, instructions, retOpcode, callOpcode }) => {
  const { formData } = useForm();

  const getInstruction = (instructionValue) => {
    if (
      (instructionValue >> (formData.instructionLength - formData.callOpcodeLength)) <<
        (formData.instructionLength - formData.callOpcodeLength) ==
      callOpcode
    )
      return "Call";
    if (
      (instructionValue >> (formData.instructionLength - formData.retOpcodeLength)) <<
        (formData.instructionLength - formData.retOpcodeLength) ==
      retOpcode
    )
      return "Return";
    return "";
  };

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
                <th>Instruction</th>
              </tr>
            </thead>
            <tbody>
              {instructions.slice(activeModalNode.start, activeModalNode.end).map((e, i) => (
                <tr key={i}>
                  <td>{i + activeModalNode.start}</td>
                  <td>0x{("0000" + e.toString(16).toUpperCase()).slice(-4)}</td>
                  <td>{getInstruction(e)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Modal.Body>
      </Modal>
    );
};

export default ModalInfo;
