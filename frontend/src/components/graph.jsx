// inspired by https://github.com/justin-coberly/dagre-d3-react/blob/master/src/index.tsx
// Wanted to make some changes which is why i did not use the dagre-d3-react npm module, as well as it being outdated

import React, { useEffect } from "react";
import dagreD3 from "dagre-d3";
import * as d3 from "d3";

const Graph = ({ graph, openModal }) => {
  useEffect(() => {
    let g = createGraph();
    drawChart(g);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graph]);

  const createGraph = () => {
    let g = new dagreD3.graphlib.Graph().setGraph({});

    graph.forEach((node) => {
      g.setNode(node.f_id, {
        label: "Function " + node.f_id,
      });
      node.calls_f_id.forEach((edge) => g.setEdge(node.f_id, edge, {}));
    });

    return g;
  };

  const drawChart = (g) => {
    // get elements
    let render = new dagreD3.render();
    let svg = d3.select("svg");
    let inner = d3.select("svg g");

    // zoom
    let zoom = d3.zoom().on("zoom", (e) => inner.attr("transform", e.transform));
    svg.call(zoom);

    // animate
    g.graph().transition = function transition(selection) {
      return selection.transition().duration(1000);
    };

    render(inner, g);

    // fit graph if below a certain size
    if (g["_nodeCount"] < 500) {
      const bounds = inner.node().getBBox();
      const parent = inner.node().parentElement || inner.node().parentNode;
      const fullWidth = parent.clientWidth || parent.parentNode.clientWidth;
      const fullHeight = parent.clientHeight || parent.parentNode.clientHeight;

      var scale = 0.9 / Math.max(bounds.width / fullWidth, bounds.height / fullHeight);
      var translate = [
        fullWidth / 2 - scale * (bounds.x + bounds.width / 2),
        fullHeight / 2 - scale * (bounds.y + bounds.height / 2),
      ];
      var transform = d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale);

      svg.transition().duration(1000).call(zoom.transform, transform);
    }

    // add on node click to return original node
    svg.selectAll("g.node").on("click", (e) => openModal(graph.find((node) => node.f_id == e.target.__data__)));
  };

  return (
    <svg width="100%" height="100%" className="dagre-d3-react">
      <g />
    </svg>
  );
};

export default Graph;
