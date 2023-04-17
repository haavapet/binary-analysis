import React from "react";

import UploadFile from "../components/uploadFile";
import ShowUploadedFile from "../components/showUploadedFile";

import "./uploadPage.css";

const UploadPage = ({ setFile, file, setToastMessage }) => {
  if (file === null) return <UploadFile setFile={setFile} setToastMessage={setToastMessage} />;
  else return <ShowUploadedFile setFile={setFile} file={file} />;
};

export default UploadPage;
