import React from "react";

const ShowUploadedFile = ({ setFile, file }) => {
  return (
    <div className="show-file">
      <span
        className="close"
        onClick={() => {
          setFile(null);
        }}
      >
        X
      </span>
      <center style={{ paddingTop: "20%" }}>
        <i
          className="fas fa-cloud-upload-alt"
          style={{ fontSize: "60px", padding: "50px" }}
        ></i>
        <div>Selected file is {file.name}</div>
      </center>
    </div>
  );
};

export default ShowUploadedFile;
