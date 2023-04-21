import { useContext } from "react";
import { Context } from "../context/store.js";

const useGraph = () => {
  const [state, setState] = useContext(Context);

  const setGraphData = (graph) => {
    setState((prev) => ({ ...prev, graphData: graph }));
  };

  let graphData = state.graphData;

  return { graphData, setGraphData };
};

export default useGraph;
