export function autoLayout(nodes) {
  const cx = 240, cy = 190, r = 130;
  const pos = {};
  nodes.forEach((n,i) => {
    const a = (2*Math.PI*i/nodes.length) - Math.PI/2;
    pos[n] = { x: cx + r*Math.cos(a), y: cy + r*Math.sin(a) };
  });
  return pos;
}

export function isIndependentSet(set, edges) {
  for (const [a,b] of edges) {
    if (set.includes(a) && set.includes(b)) return false;
  }
  return true;
}

