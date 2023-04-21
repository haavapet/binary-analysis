import { useContext } from "react";
import { Context } from "../context/store.js";

const useToast = () => {
  const [state, setState] = useContext(Context);

  const setToastMessage = (message) => {
    setState(() => ({ ...state, toastMessage: message }));
  };

  let toastMessage = state.toastMessage;

  return { toastMessage, setToastMessage };
};

export default useToast;
