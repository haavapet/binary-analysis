import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const UploadFile = ({ setFile, file, setToastMessage }) => {
  const [dragOver, setDragOver] = useState(false);

  const onDrop = useCallback(
    (acceptedFile) => {
      if (acceptedFile.length == 1) {
        acceptedFile.forEach((file) => {
          const reader = new FileReader();

          reader.onabort = () => setToastMessage("File reading was aborted");
          reader.onerror = () => setToastMessage("File reading has failed");
          reader.onload = () => {
            setFile(file);
          };

          reader.readAsDataURL(file);
        });
      } else {
        setToastMessage("Please only select 1 file for analysis");
      }
    },
    [setFile, setToastMessage]
  );

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    // accept: {
    //   "application/*": [".exe", ".ch8"],
    // },
    noClick: true, // Prevent open dialog using js
  });

  if (file == null)
    return (
      <label {...getRootProps()} style={{ height: "90%", width: "90%" }}>
        <input {...getInputProps()} />
        <div
          className={dragOver ? "drag-image drag-image-active" : "drag-image"}
          onDragEnter={() => setDragOver(true)}
          onDragOver={() => setDragOver(true)}
          onDragLeave={() => setDragOver(false)}
          onDragEnd={() => setDragOver(false)}
          onBlur={() => setDragOver(false)}
          onDrop={() => setDragOver(false)}
        >
          <i className="fas fa-cloud-upload-alt"></i>
          <h6>Drag & Drop File Here</h6>
          <span>OR</span>
          <div className="btn">Browse File</div>
        </div>
      </label>
    );
  else
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

export default UploadFile;
