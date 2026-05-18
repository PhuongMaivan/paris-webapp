import { useState } from "react";
import { C } from "./constants/colors";
import { EXAMPLES } from "./data/examples";
import { autoLayout, isIndependentSet } from "./utils/graphUtils";
import GraphCanvas from "./components/GraphCanvas";
import SequencePlayer from "./components/SequencePlayer";
import { ALGO_TABS, ALGO_CONTENT } from "./components/AlgoExplain";

export default function PARISWebapp() {
  const [tab, setTab] = useState("solve");
  const [example, setExample] = useState(EXAMPLES[0]);
  const [nodes, setNodes] = useState(EXAMPLES[0].nodes);
  const [edges, setEdges] = useState(EXAMPLES[0].edges);
  const [startSet, setStartSet] = useState(EXAMPLES[0].start);
  const [goalSet, setGoalSet] = useState(EXAMPLES[0].goal);
  const [positions, setPositions] = useState(autoLayout(EXAMPLES[0].nodes));
  const [editMode, setEditMode] = useState("drag");
  const [selectTarget, setSelectTarget] = useState("start");
  const [addingEdge, setAddingEdge] = useState(null);
  const [solved, setSolved] = useState(false);
  const [solving, setSolving] = useState(false);
  const [sequence, setSequence] = useState([]);
  const [reachable, setReachable] = useState(null);
  const [algoTab, setAlgoTab] = useState("State Model");
  const [nodeCounter, setNodeCounter] = useState(10);

const loadExample = (ex) => {
  setExample(ex); // Cập nhật cả object example để đồng bộ UI nút bấm
  setNodes(ex.nodes);
  setEdges(ex.edges);
  setStartSet(ex.start);
  setGoalSet(ex.goal);
  
  // QUAN TRỌNG: Cập nhật lại vị trí các node theo dữ liệu mới
  setPositions(autoLayout(ex.nodes)); 
  
  setSolved(false);
  setReachable(null);
  setSequence([]);
};
  
  const handleToggleNode = (n) => {
    if (editMode !== "select") return;
    if (selectTarget === "start") {
      setStartSet(s => s.includes(n) ? s.filter(x=>x!==n) : [...s, n]);
    } else {
      setGoalSet(s => s.includes(n) ? s.filter(x=>x!==n) : [...s, n]);
    }
    setSolved(false);
  };

  const handleAddNode = () => {
    const maxId = nodes.length > 0 ? Math.max(...nodes) : -1;
    const n = maxId + 1;
    setNodes(ns => [...ns, n]);
    const angle = Math.random()*2*Math.PI;
    setPositions(p => ({ ...p, [n]: { x: 240 + 100*Math.cos(angle), y: 190 + 100*Math.sin(angle) }}));
  };

  const handleAddEdge = (a, b) => {
    if (edges.some(([x,y]) => (x===a&&y===b)||(x===b&&y===a))) return;
    setEdges(e => [...e, [a,b]]);
  };

  const handleRemoveEdge = (a, b) => {
    setEdges(e => e.filter(([x,y]) => !((x===a&&y===b)||(x===b&&y===a))));
  };

  const handleSolve = async () => {
  setSolving(true);
  try {
    // 1. Tự động kiểm tra xem có phải đang chạy ở máy local không
    const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
    
    // 2. Nếu là local thì hướng thẳng về cổng backend 8000, nếu là Railway thì tự lấy link mạng công khai
    const apiUrl = isLocalhost 
      ? "http://localhost:8000/solve" 
      : `${window.location.origin}/solve`;

    // 3. Thực hiện gọi API chuẩn xác theo môi trường
    const res = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes,
        edges,
        start: startSet,
        goal: goalSet
      })
    });
    const data = await res.json();
    setReachable(data.reachable);
    setSequence(data.sequence || []);
    setSolved(true);
  } catch (err) {
    alert("Backend error: " + err.message);
  } finally {
    setSolving(false);
  }
};
  const startValid = isIndependentSet(startSet, edges);
  const goalValid = isIndependentSet(goalSet, edges);

  return (
    <div style={{
      minHeight:"100vh", background:C.bg, color:C.text,
      fontFamily:"'IBM Plex Sans', system-ui, sans-serif",
    }}>
      <style>{`
          @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600;700&family=Space+Grotesk:wght@700&display=swap');

          html, body, #root {
            margin: 0;
            padding: 0;
            background: #0a0e1a;
            overflow-x: hidden;
          }

          * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
          }

          ::-webkit-scrollbar {
            width: 6px;
            background: #0a0e1a;
          }

          ::-webkit-scrollbar-thumb {
            background: #1e2d45;
            border-radius: 3px;
          }

          button:hover {
            opacity: 0.85;
          }
        `}</style>

      {/* Header */}
      <div style={{borderBottom:`1px solid ${C.border}`, padding:"14px 24px",
        display:"flex", alignItems:"center", gap:16, background:"#0d1526",
        position:"sticky", top:0, zIndex:100}}>
        <div>
          <span style={{fontFamily:"'Space Grotesk',sans-serif", fontSize:22,
            fontWeight:700, color:C.accent, letterSpacing:"-0.5px"}}>PARIS</span>
          <span style={{color:C.muted, fontSize:13, marginLeft:10}}>
            Planning Algorithms for Reconfiguring Independent Sets
          </span>
        </div>
        <div style={{marginLeft:"auto", display:"flex", gap:4}}>
          {[["solve","Solver"], ["explain","Algorithm"], ["glossary","Glossary"]].map(([id,label]) => (
            <button key={id} onClick={() => setTab(id)}
              style={{padding:"6px 16px", borderRadius:8, border:"none", cursor:"pointer",
                fontFamily:"'IBM Plex Mono',monospace", fontSize:13, fontWeight:700,
                background: tab===id ? C.accent : "transparent",
                color: tab===id ? "#000" : C.muted,
                transition:"all .2s"}}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* ── TAB: SOLVE ── */}
      {tab === "solve" && (
        <div style={{padding:24, maxWidth:1100, margin:"0 auto"}}>
          <div style={{display:"flex", gap:20, flexWrap:"wrap"}}>

            {/* Left: Examples + Graph Editor */}
            <div style={{flex:"1 1 480px"}}>
              {/* Examples */}
              <div style={{marginBottom:16}}>
                <div style={{color:C.muted, fontSize:12, fontFamily:"'IBM Plex Mono',monospace",
                  marginBottom:8, letterSpacing:"0.1em"}}>EXAMPLE LIBRARY</div>
                <div style={{display:"flex", gap:8, flexWrap:"wrap"}}>
                  {EXAMPLES.map(ex => (
                    <button key={ex.id} onClick={() => loadExample(ex)}
                      style={{padding:"6px 12px", borderRadius:8, border:`1px solid ${example.id===ex.id ? C.accent : C.border}`,
                        background: example.id===ex.id ? C.accent+"22" : "#0d1526",
                        color: example.id===ex.id ? C.accent : C.muted,
                        fontSize:12, cursor:"pointer", fontFamily:"'IBM Plex Mono',monospace",
                        transition:"all .2s"}}>
                      {ex.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Toolbar */}
              <div style={{display:"flex", gap:6, marginBottom:12, flexWrap:"wrap"}}>
                {[
                  ["drag","✥ Drag", "Move nodes"],
                  ["edge","⚡ Edge", "Add/remove edges"],
                ].map(([mode,label]) => (
                  <button key={mode} onClick={() => { setEditMode(mode); setAddingEdge(null); }}
                    style={{padding:"5px 12px", borderRadius:7, border:`1px solid ${editMode===mode ? C.accent : C.border}`,
                      background: editMode===mode ? C.accent+"22" : "#0d1526",
                      color: editMode===mode ? C.accent : C.muted,
                      fontSize:12, cursor:"pointer", fontFamily:"'IBM Plex Mono',monospace"}}>
                    {label}
                  </button>
                ))}
                {[["start","▣ Start", C.accent], ["goal","◎ Goal", C.green]].map(([tgt,label,col]) => (
                  <button key={tgt} onClick={() => { setEditMode("select"); setSelectTarget(tgt); }}
                    style={{padding:"5px 12px", borderRadius:7,
                      border:`1px solid ${editMode==="select"&&selectTarget===tgt ? col : C.border}`,
                      background: editMode==="select"&&selectTarget===tgt ? col+"22" : "#0d1526",
                      color: editMode==="select"&&selectTarget===tgt ? col : C.muted,
                      fontSize:12, cursor:"pointer", fontFamily:"'IBM Plex Mono',monospace"}}>
                    {label}
                  </button>
                ))}
                <button onClick={handleAddNode}
                  style={{padding:"5px 12px", borderRadius:7, border:`1px solid ${C.border}`,
                    background:"#0d1526", color:C.muted, fontSize:12, cursor:"pointer",
                    fontFamily:"'IBM Plex Mono',monospace"}}>
                  + Node
                </button>
              </div>

              <GraphCanvas
                nodes={nodes} edges={edges} positions={positions}
                setPositions={setPositions}
                startSet={startSet} goalSet={goalSet}
                currentSet={solved && sequence.length ? sequence[0] : startSet}
                mode={editMode} onToggleNode={handleToggleNode}
                onAddEdge={handleAddEdge} onRemoveEdge={handleRemoveEdge}
                addingEdge={addingEdge} setAddingEdge={setAddingEdge}/>

              {/* Legend */}
              <div style={{display:"flex", gap:16, marginTop:10, fontSize:12, color:C.muted}}>
                {[[C.token,"Start token"],[C.green,"Goal vertex"],[C.yellow,"Both"],[C.red,"Conflict"]].map(([col,label]) => (
                  <span key={label} style={{display:"flex",alignItems:"center",gap:5}}>
                    <span style={{width:10,height:10,borderRadius:"50%",background:col,display:"inline-block"}}/>
                    {label}
                  </span>
                ))}
              </div>
            </div>

            {/* Right: Controls + Result */}
            <div style={{flex:"1 1 300px", display:"flex", flexDirection:"column", gap:16}}>

              {/* Status */}
              <div style={{background:C.panel, borderRadius:12, padding:16, border:`1px solid ${C.border}`}}>
                <div style={{color:C.muted, fontSize:12, fontFamily:"'IBM Plex Mono',monospace",
                  marginBottom:10, letterSpacing:"0.1em"}}>INSTANCE STATUS</div>
                {[
                  ["Start set", `[${startSet.join(", ")}]`, startValid ? C.green : C.red, startValid ? "✓ valid" : "✗ adjacent pair"],
                  ["Goal set", `[${goalSet.join(", ")}]`, goalValid ? C.green : C.red, goalValid ? "✓ valid" : "✗ adjacent pair"],
                  ["Vertices", nodes.length, C.accent, ""],
                  ["Edges", edges.length, C.accent, ""],
                ].map(([label, val, col, note]) => (
                  <div key={label} style={{display:"flex", justifyContent:"space-between",
                    padding:"5px 0", borderBottom:`1px solid ${C.border}22`}}>
                    <span style={{color:C.muted, fontSize:13}}>{label}</span>
                    <span style={{color:col, fontFamily:"'IBM Plex Mono',monospace", fontSize:13}}>
                      {String(val)} {note && <span style={{fontSize:11, opacity:.7}}>{note}</span>}
                    </span>
                  </div>
                ))}
              </div>

              {/* Solve button */}
              <button onClick={handleSolve}
                disabled={!startValid || !goalValid || solving}
                style={{padding:"14px 0", borderRadius:12, border:"none", cursor:"pointer",
                  background: solving ? C.muted : (!startValid||!goalValid) ? "#1e2d45" : `linear-gradient(135deg, ${C.accent}, ${C.accentDim})`,
                  color: solving||(!startValid||!goalValid) ? "#0a0e1a" : "#000",
                  fontFamily:"'IBM Plex Mono',monospace", fontWeight:700, fontSize:16,
                  letterSpacing:"0.05em", transition:"all .3s",
                  boxShadow: !solving&&startValid&&goalValid ? `0 0 20px ${C.accent}44` : "none"}}>
                {solving ? "⟳  PARIS SOLVING..." : "▶  RUN PARIS SOLVER"}
              </button>

              {solving && (
                <div style={{background:C.panel, borderRadius:10, padding:14,
                  border:`1px solid ${C.border}`, fontFamily:"'IBM Plex Mono',monospace", fontSize:12}}>
                  {["Encoding ISR → PDDL/SAS+...","Running GBFS + Landmarks...","Tracing reconfiguration sequence..."].map((msg,i) => (
                    <div key={i} style={{color: i===0 ? C.green : i===1 ? C.accent : C.muted,
                      marginBottom:4, animation:`fadein .4s ${i*0.5}s both`}}>
                      {i < 2 ? "✓" : "⟳"} {msg}
                    </div>
                  ))}
                </div>
              )}

              {/* Result */}
              {solved && (
                <div style={{background:C.panel, borderRadius:12, padding:16,
                  border:`1px solid ${reachable ? C.green : C.red}44`}}>
                  <div style={{display:"flex", alignItems:"center", gap:10, marginBottom:12}}>
                    <div style={{width:40,height:40,borderRadius:8,
                      background: reachable ? C.green+"22" : C.red+"22",
                      border:`1px solid ${reachable ? C.green : C.red}`,
                      display:"flex", alignItems:"center", justifyContent:"center",
                      fontSize:20}}>
                      {reachable ? "✓" : "⊗"}
                    </div>
                    <div>
                      <div style={{color: reachable ? C.green : C.red,
                        fontFamily:"'IBM Plex Mono',monospace", fontWeight:700, fontSize:15}}>
                        {reachable ? "REACHABLE" : "UNREACHABLE"}
                      </div>
                      <div style={{color:C.muted, fontSize:12}}>
                        {reachable ? `Sequence length: ${sequence.length-1} steps` : "No path exists between start and goal"}
                      </div>
                    </div>
                  </div>
                  <SequencePlayer sequence={sequence} edges={edges}
                    positions={positions} goalSet={goalSet}/>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── TAB: ALGORITHM ── */}
      {tab === "explain" && (
        <div style={{padding:24, maxWidth:900, margin:"0 auto"}}>
          <div style={{marginBottom:20}}>
            <div style={{fontFamily:"'Space Grotesk',sans-serif", fontSize:24, fontWeight:700,
              color:C.accent, marginBottom:6}}>How PARIS Works</div>
            <div style={{color:C.muted, fontSize:14}}>
              A planning-based solver for Independent Set Reconfiguration under token jump.
            </div>
          </div>

          {/* Pipeline diagram */}
          <div style={{display:"flex", alignItems:"center", gap:0, marginBottom:24,
            background:C.panel, borderRadius:12, padding:"14px 16px", border:`1px solid ${C.border}`,
            overflowX:"auto"}}>
            {[
              ["ISR Instance", C.muted, "Graph G, S_start, S_goal"],
              ["→", C.border, ""],
              ["PDDL/SAS+", C.accent, "Variables, actions, preconditions"],
              ["→", C.border, ""],
              ["Planner", C.yellow, "GBFS / A* / BDD / Counter"],
              ["→", C.border, ""],
              ["Plan", C.green, "Sequence of token jumps"],
            ].map(([label, col, sub], i) => (
              label === "→" ? (
                <div key={i} style={{color:C.border, fontSize:24, padding:"0 8px", flexShrink:0}}>→</div>
              ) : (
                <div key={i} style={{textAlign:"center", minWidth:110, padding:"4px 8px"}}>
                  <div style={{color:col, fontFamily:"'IBM Plex Mono',monospace", fontWeight:700, fontSize:13}}>{label}</div>
                  <div style={{color:C.muted, fontSize:11, marginTop:3}}>{sub}</div>
                </div>
              )
            ))}
          </div>

          {/* Algo tabs */}
          <div style={{display:"flex", gap:4, marginBottom:16}}>
            {ALGO_TABS.map(t => (
              <button key={t} onClick={() => setAlgoTab(t)}
                style={{padding:"7px 16px", borderRadius:8, border:"none", cursor:"pointer",
                  fontFamily:"'IBM Plex Mono',monospace", fontSize:13, fontWeight:700,
                  background: algoTab===t ? C.accent : "#0d1526",
                  color: algoTab===t ? "#000" : C.muted, transition:"all .2s"}}>
                {ALGO_CONTENT[t].icon} {t}
              </button>
            ))}
          </div>

          <div style={{background:C.panel, borderRadius:12, padding:20, border:`1px solid ${C.border}`}}>
            {ALGO_CONTENT[algoTab].content}
          </div>
        </div>
      )}

      {/* ── TAB: GLOSSARY ── */}
      {tab === "glossary" && (
        <div style={{padding:24, maxWidth:800, margin:"0 auto"}}>
          <div style={{fontFamily:"'Space Grotesk',sans-serif", fontSize:24, fontWeight:700,
            color:C.accent, marginBottom:20}}>Glossary</div>
          {[
            ["Independent Set", "A set of vertices in a graph with no two vertices adjacent (connected by an edge)."],
            ["Token Jump (TJ)", "A reconfiguration rule: move one token from vertex u to any non-adjacent vertex v, keeping the result a valid independent set."],
            ["State Graph", "A graph where each node is a valid configuration (IS) and edges represent valid transitions (token jumps)."],
            ["ISR", "Independent Set Reconfiguration — deciding if two IS can be connected by a sequence of token jumps."],
            ["PDDL", "Planning Domain Definition Language — a standard format to describe classical planning problems (states, actions, goals)."],
            ["SAS+", "A compact multi-valued planning formalism used internally by planners like Fast Downward."],
            ["Heuristic Search", "Search guided by an estimate h(s) of the cost to reach the goal from state s."],
            ["Landmarks", "Facts that must hold at some point in every plan — used to compute admissible heuristics."],
            ["BDD", "Binary Decision Diagram — a compact data structure to represent sets of states symbolically for efficient search."],
            ["Symbolic Search", "Search that operates on sets of states represented as BDDs rather than individual states."],
            ["Counter Abstraction", "An abstraction that counts tokens per neighborhood class, ignoring exact positions — used to detect unreachability."],
            ["Portfolio", "Running multiple solver configurations sequentially with timeouts; stop when any config succeeds."],
            ["Reachable / Unreachable", "Whether a goal IS can be reached from a start IS via token jumps. PARIS proves both outcomes."],
            ["CoRe Challenge", "Combinatorial Reconfiguration Challenge 2022 — defines benchmark instances and file formats (*.col, *.dat, *.out)."],
          ].map(([term, def]) => (
            <div key={term} style={{padding:"12px 0", borderBottom:`1px solid ${C.border}`}}>
              <div style={{color:C.accent, fontFamily:"'IBM Plex Mono',monospace",
                fontWeight:700, fontSize:14, marginBottom:4}}>{term}</div>
              <div style={{color:C.muted, fontSize:14, lineHeight:1.7}}>{def}</div>
            </div>
          ))}
        </div>
      )}

      {/* Footer */}
      <div style={{borderTop:`1px solid ${C.border}`, padding:"14px 24px", marginTop:40,
        display:"flex", justifyContent:"space-between", color:C.muted, fontSize:12,
        fontFamily:"'IBM Plex Mono',monospace"}}>
        <span>PARIS — Christen et al., ECAI 2023</span>
        <span style={{color:C.border}}>Frontend demo — connect to backend for real solver execution</span>
      </div>
    </div>
  );
}