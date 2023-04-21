import React from "react";

import useForm from "../hooks/useForm";

import UploadFile from "../components/uploadFile";
import ShowUploadedFile from "../components/showUploadedFile";

import "../styles/uploadPage.css";

const UploadPage = () => {
  const { file } = useForm();

  if (file === null) return <UploadFile />;
  else return <ShowUploadedFile />;
};

export default UploadPage;
