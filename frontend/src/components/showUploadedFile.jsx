import React from "react";

import useForm from "../hooks/useForm";

const ShowUploadedFile = () => {
  const { file, setFormElement } = useForm();

  return (
    <div className="show-file">
      <span
        className="close"
        onClick={() => {
          setFormElement("file", null);
        }}
      >
        X
      </span>
      <center style={{ paddingTop: "20%" }}>
        <i className="fas fa-cloud-upload-alt" style={{ fontSize: "60px", padding: "50px" }}></i>
        <div>Selected file is {file.name}</div>
      </center>
    </div>
  );
};

export default ShowUploadedFile;
