import { useContext } from "react";
import { Context } from "../context/store.js";

const useForm = () => {
  const [state, setState] = useContext(Context);

  const setFormElement = (name, value) => {
    setState((prev) => ({ ...prev, formData: { ...prev.formData, [name]: value } }));
  };

  const validateForm = () => {
    const form = document.getElementById("binaryInfoForm");
    setState({ ...state, formValidated: true });
    return form.checkValidity();
  };

  let formData = state.formData;
  let file = state.formData.file;
  let formValidated = state.formValidated;

  return { formData, setFormElement, file, formValidated, validateForm };
};

export default useForm;
