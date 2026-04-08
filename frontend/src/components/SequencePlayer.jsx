import { useState, useRef, useEffect } from "react";
import { C } from "../constants/colors";

export default function SequencePlayer({ sequence, edges, positions, goalSet }) {
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const intervalRef = useRef();

  useEffect(() => {
    setStep(0); setPlaying(false);
  }, [sequence]);

  useEffect(() => {
    if (playing) {
      intervalRef.current = setInterval(() => {
        setStep(s => {
          if (s >= sequence.length - 1) { setPlaying(false); return s; }
          return s + 1;
        });
      }, 1200);
    }
    return () => clearInterval(intervalRef.current);
  }, [playing, sequence.length]);

  if (!sequence.length) return (
    <div style={{padding:24, textAlign:"center", color: C.red, fontFamily:"'IBM Plex Mono',monospace"}}>
      <div style={{fontSize:32}}>⊗</div>
      <div style={{marginTop:8}}>UNREACHABLE — no reconfiguration sequence exists.</div>
    </div>
  );

  const cur = sequence[step];
  const prev = step > 0 ? sequence[step-1] : null;
  const removed = prev ? prev.filter(n => !cur.includes(n)) : [];
  const added = prev ? cur.filter(n => !prev.includes(n)) : [];

  return (
    <div>
      {/* Mini graph */}
      <div style={{display:"flex", justifyContent:"center", marginBottom:12}}>
        <svg width="320" height="220" style={{background:"#0d1526", borderRadius:10, border:`1px solid ${C.border}`}}>
          <defs>
            <filter id="glow2">
              <feGaussianBlur stdDeviation="3" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          {edges.map(([a,b],i) => {
            const pa = positions[a], pb = positions[b];
            if (!pa || !pb) return null;
            const scale = n => ({ x: n.x * 0.65 + 10, y: n.y * 0.55 + 10 });
            const sa = scale(pa), sb = scale(pb);
            return <line key={i} x1={sa.x} y1={sa.y} x2={sb.x} y2={sb.y}
              stroke={C.border} strokeWidth={1.5}/>;
          })}
          {Object.keys(positions).map(n => {
            const ni = parseInt(n);
            const p = positions[ni];
            if (!p) return null;
            const sx = p.x * 0.65 + 10, sy = p.y * 0.55 + 10;
            const inCur = cur.includes(ni);
            const isAdded = added.includes(ni);
            const isRemoved = removed.includes(ni);
            const isGoal = goalSet.includes(ni);
            return (
              <g key={n}>
                {inCur && <circle cx={sx} cy={sy} r={18} fill={C.token} opacity={0.2} filter="url(#glow2)"/>}
                <circle cx={sx} cy={sy} r={13}
                  fill={isAdded ? C.green : isRemoved ? C.red : inCur ? C.token : "#1e3a5f"}
                  stroke={isGoal && inCur ? C.yellow : isGoal ? C.green : inCur ? C.accentDim : C.border}
                  strokeWidth={2}/>
                <text x={sx} y={sy+4} textAnchor="middle"
                  fill={inCur ? "#000" : C.muted} fontSize={11} fontWeight="700"
                  fontFamily="'IBM Plex Mono',monospace">{n}</text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Step info */}
      <div style={{background:"#0d1932", border:`1px solid ${C.border}`, borderRadius:8,
        padding:"10px 16px", marginBottom:12, fontFamily:"'IBM Plex Mono',monospace", fontSize:13}}>
        <span style={{color:C.muted}}>Step {step}/{sequence.length-1} — State: </span>
        <span style={{color:C.accent}}>[{cur.join(", ")}]</span>
        {prev && (
          <span style={{marginLeft:12}}>
            {removed.length > 0 && <span style={{color:C.red}}>  −{removed[0]} </span>}
            {added.length > 0 && <span style={{color:C.green}}>  +{added[0]}</span>}
          </span>
        )}
        {step === sequence.length-1 && (
          <span style={{marginLeft:12, color:C.green}}>✓ GOAL REACHED</span>
        )}
      </div>

      {/* Timeline */}
      <div style={{display:"flex", gap:4, marginBottom:12, flexWrap:"wrap"}}>
        {sequence.map((s,i) => (
          <button key={i} onClick={() => setStep(i)}
            style={{padding:"4px 10px", borderRadius:6, border:"none", cursor:"pointer", fontSize:12,
              fontFamily:"'IBM Plex Mono',monospace", fontWeight:"700",
              background: i===step ? C.accent : i < step ? "#1a3a5c" : "#0d1932",
              color: i===step ? "#000" : i < step ? C.accentDim : C.muted,
              transition:"all .2s"}}>
            s{i}
          </button>
        ))}
      </div>

      {/* Controls */}
      <div style={{display:"flex", gap:8}}>
        {[["⏮", () => setStep(0)], ["⏪", () => setStep(s => Math.max(0,s-1))],
          [playing ? "⏸" : "▶", () => setPlaying(p => !p)],
          ["⏩", () => setStep(s => Math.min(sequence.length-1, s+1))],
          ["⏭", () => setStep(sequence.length-1)]
        ].map(([label, fn], i) => (
          <button key={i} onClick={fn}
            style={{flex:1, padding:"8px 0", background:"#0d1932", border:`1px solid ${C.border}`,
              borderRadius:8, color: label === "▶" || label === "⏸" ? C.accent : C.text,
              fontSize:16, cursor:"pointer", transition:"background .2s"}}
            onMouseOver={e => e.target.style.background="#1a2a45"}
            onMouseOut={e => e.target.style.background="#0d1932"}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

