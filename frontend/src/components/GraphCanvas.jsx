import { useRef, useCallback } from "react";
import { C } from "../constants/colors";
export default function GraphCanvas({ nodes, edges, positions, setPositions,
  startSet, goalSet, currentSet, mode, onToggleNode, onAddEdge, onRemoveEdge,
  addingEdge, setAddingEdge }) {

  const svgRef = useRef();
  const dragging = useRef(null);

  const getNodeColor = (n) => {
    if (currentSet.includes(n)) return C.token;
    if (goalSet.includes(n)) return C.goal;
    return "#1e3a5f";
  };

  const getNodeStroke = (n) => {
    if (startSet.includes(n) && goalSet.includes(n)) return C.yellow;
    if (startSet.includes(n)) return C.token;
    if (goalSet.includes(n)) return C.green;
    return C.border;
  };

  const onMouseDown = (e, n) => {
    if (mode === "edge") {
      if (!addingEdge) { setAddingEdge(n); return; }
      if (addingEdge !== n) onAddEdge(addingEdge, n);
      setAddingEdge(null);
      return;
    }
    if (mode === "select") { onToggleNode(n); return; }
    dragging.current = { node: n, ox: e.clientX, oy: e.clientY };
    e.stopPropagation();
  };

  const onMouseMove = useCallback((e) => {
    if (!dragging.current) return;
    const { node } = dragging.current;
    const svg = svgRef.current;
    const rect = svg.getBoundingClientRect();
    setPositions(p => ({ ...p, [node]: {
      x: Math.max(20, Math.min(460, e.clientX - rect.left)),
      y: Math.max(20, Math.min(360, e.clientY - rect.top)),
    }}));
  }, [setPositions]);

  const onMouseUp = () => { dragging.current = null; };

  return (
    <svg ref={svgRef} width="480" height="380"
      style={{ background: "#0d1526", borderRadius: 12, border: `1px solid ${C.border}`, cursor: mode === "drag" ? "crosshair" : "default" }}
      onMouseMove={onMouseMove} onMouseUp={onMouseUp}>

      {/* Grid */}
      <defs>
        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
          <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1a2744" strokeWidth="0.5"/>
        </pattern>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <rect width="480" height="380" fill="url(#grid)"/>

      {/* Edges */}
      {edges.map(([a,b],i) => {
        const pa = positions[a], pb = positions[b];
        if (!pa || !pb) return null;
        const active = currentSet.includes(a) && currentSet.includes(b);
        return (
          <g key={i}>
            <line x1={pa.x} y1={pa.y} x2={pb.x} y2={pb.y}
              stroke={active ? C.red : C.border} strokeWidth={active ? 2.5 : 1.5}
              strokeDasharray={active ? "5,3" : "none"} opacity={0.8}/>
            {mode === "edge" && (
              <line x1={pa.x} y1={pa.y} x2={pb.x} y2={pb.y}
                stroke="transparent" strokeWidth={12}
                style={{cursor:"pointer"}} onClick={() => onRemoveEdge(a,b)}/>
            )}
          </g>
        );
      })}

      {/* Adding edge preview */}
      {addingEdge && positions[addingEdge] && (
        <circle cx={positions[addingEdge].x} cy={positions[addingEdge].y}
          r={22} fill="none" stroke={C.accent} strokeWidth={2} strokeDasharray="4,2" opacity={0.6}/>
      )}

      {/* Nodes */}
      {nodes.map(n => {
        const p = positions[n];
        if (!p) return null;
        const inCurrent = currentSet.includes(n);
        return (
          <g key={n} style={{cursor:"pointer"}}
            onMouseDown={e => onMouseDown(e, n)}>
            {inCurrent && (
              <circle cx={p.x} cy={p.y} r={22} fill={C.token} opacity={0.15} filter="url(#glow)"/>
            )}
            <circle cx={p.x} cy={p.y} r={16}
              fill={getNodeColor(n)} stroke={getNodeStroke(n)} strokeWidth={2.5}/>
            <text x={p.x} y={p.y+5} textAnchor="middle"
              fill={inCurrent ? "#000" : C.text} fontSize={13} fontWeight="700"
              fontFamily="'IBM Plex Mono', monospace">{n}</text>
            {goalSet.includes(n) && !inCurrent && (
              <circle cx={p.x} cy={p.y} r={19} fill="none"
                stroke={C.green} strokeWidth={1.5} strokeDasharray="3,2" opacity={0.7}/>
            )}
          </g>
        );
      })}
    </svg>
  );
}
