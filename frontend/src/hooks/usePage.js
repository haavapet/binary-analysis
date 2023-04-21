import { useContext } from "react";
import { Context } from "../context/store.js";

const usePage = () => {
  const [state, setState] = useContext(Context);

  const incrementPage = () => {
    setState((prev) => ({ ...prev, page: prev.page + 1 }));
  };

  const decrementPage = () => {
    setState((prev) => ({ ...prev, page: prev.page - 1 }));
  };

  let page = state.page;

  return { page, incrementPage, decrementPage };
};

export default usePage;
