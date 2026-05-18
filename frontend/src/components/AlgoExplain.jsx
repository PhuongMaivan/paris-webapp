import { C } from "../constants/colors";
export const ALGO_TABS = ["State Model", "PDDL Encoding", "Search", "Portfolio"];

export const ALGO_CONTENT = {
  "State Model": {
    icon: "⬡",
    content: (
      <div>
        <p style={{color:C.text, lineHeight:1.7, marginBottom:16}}>
          An <b style={{color:C.accent}}>Independent Set</b> is a set of vertices with no two adjacent.
          In ISR (token jump), each vertex in the set holds a token.
        </p>
        <div style={{background:"#0d1932", borderRadius:8, padding:16, marginBottom:16, fontFamily:"'IBM Plex Mono',monospace", fontSize:13}}>
          <div style={{color:C.green, marginBottom:8}}>State = valid independent set IS ⊆ V</div>
          <div style={{color:C.muted}}>• |IS| = k  (fixed size)</div>
          <div style={{color:C.muted}}>• ∀ u,v ∈ IS: (u,v) ∉ E</div>
        </div>
        <div style={{background:"#0d1932", borderRadius:8, padding:16, fontFamily:"'IBM Plex Mono',monospace", fontSize:13}}>
          <div style={{color:C.yellow, marginBottom:8}}>Transition (token jump):</div>
          <div style={{color:C.muted}}>IS → IS' where IS' = IS ∖ &#123;u&#125; ∪ &#123;v&#125;</div>
          <div style={{color:C.muted, marginTop:4}}>• v ∉ IS,  v ∉ N(IS ∖ &#123;u&#125;)</div>
          <div style={{color:C.muted}}>• IS' must still be independent</div>
        </div>
      </div>
    )
  },
  "PDDL Encoding": {
    icon: "⚙",
    content: (
      <div>
        <p style={{color:C.text, lineHeight:1.7, marginBottom:12}}>
          PARIS encodes ISR as a classical planning problem in <b style={{color:C.accent}}>PDDL/SAS+</b>:
        </p>
        {[
          ["State variables", "token-at(v) ∈ {0,1} for each vertex v", C.accent],
          ["Initial state", "token-at(v) = 1 iff v ∈ S_start", C.green],
          ["Goal condition", "token-at(v) = 1 iff v ∈ S_goal", C.yellow],
          ["Action jump(u→v)", "pre: token-at(u)=1, token-at(v)=0,\n  ∀w∈N(v): token-at(w)=0\neff: token-at(u):=0, token-at(v):=1", C.token],
        ].map(([label, val, col]) => (
          <div key={label} style={{background:"#0d1932", borderRadius:8, padding:12,
            marginBottom:10, fontFamily:"'IBM Plex Mono',monospace", fontSize:12}}>
            <div style={{color:col, fontWeight:700, marginBottom:4}}>{label}</div>
            <pre style={{color:C.muted, margin:0, whiteSpace:"pre-wrap"}}>{val}</pre>
          </div>
        ))}
      </div>
    )
  },
  "Search": {
    icon: "🔍",
    content: (
      <div>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:10, marginBottom:12}}>
          {[
            ["GBFS + Landmarks", "Greedy Best-First Search guided by landmark heuristic h^lm. Fast, not optimal.", C.accent],
            ["A* + Landmarks", "Optimal search using h^lm as admissible heuristic. Guarantees shortest sequence.", C.green],
            ["Symbolic (BDD)", "Represents sets of states as Binary Decision Diagrams. Efficient for wide search.", C.yellow],
            ["Counter Abstraction", "Detects UNREACHABLE instances by counting tokens without tracking positions.", C.red],
          ].map(([title, desc, col]) => (
            <div key={title} style={{background:"#0d1932", borderRadius:8, padding:12, border:`1px solid ${col}33`}}>
              <div style={{color:col, fontWeight:700, fontSize:13, marginBottom:6, fontFamily:"'IBM Plex Mono',monospace"}}>{title}</div>
              <div style={{color:C.muted, fontSize:12, lineHeight:1.6}}>{desc}</div>
            </div>
          ))}
        </div>
        <div style={{background:"#0d1932", borderRadius:8, padding:12, fontFamily:"'IBM Plex Mono',monospace", fontSize:12, color:C.muted}}>
          <span style={{color:C.text}}>Heuristic landmarks:</span> facts that must be true at some point on any plan path. Used to estimate remaining cost h(s).
        </div>
      </div>
    )
  },
  "Portfolio": {
    icon: "📋",
    content: (
      <div>
        <p style={{color:C.text, lineHeight:1.7, marginBottom:12}}>
          PARIS runs multiple solver configurations in sequence, each with a <b style={{color:C.accent}}>timeout</b>:
        </p>
        {[
          ["Config 1", "GBFS + Landmarks", "5s", C.accent, "Fast solution, suboptimal"],
          ["Config 2", "Symbolic BDD forward", "10s", C.yellow, "Wide breadth search"],
          ["Config 3", "Counter abstraction", "5s", C.red, "Prove unreachable"],
          ["Config 4", "A* + Landmarks", "∞", C.green, "Optimal solution"],
        ].map(([id, name, time, col, desc]) => (
          <div key={id} style={{display:"flex", alignItems:"center", gap:10, marginBottom:8,
            background:"#0d1932", borderRadius:8, padding:"10px 14px"}}>
            <div style={{width:36, height:36, borderRadius:6, background:col+"22",
              border:`1px solid ${col}`, display:"flex", alignItems:"center", justifyContent:"center",
              color:col, fontFamily:"'IBM Plex Mono',monospace", fontSize:11, fontWeight:700}}>{id}</div>
            <div style={{flex:1}}>
              <div style={{color:C.text, fontSize:13, fontFamily:"'IBM Plex Mono',monospace"}}>{name}</div>
              <div style={{color:C.muted, fontSize:11}}>{desc}</div>
            </div>
            <div style={{color:col, fontFamily:"'IBM Plex Mono',monospace", fontSize:12, fontWeight:700}}>⏱ {time}</div>
          </div>
        ))}
        <div style={{color:C.muted, fontSize:12, marginTop:8}}>
          If any config finds a solution or proves unreachability → stop immediately. Otherwise continue to next config.
        </div>
      </div>
    )
  }
};
