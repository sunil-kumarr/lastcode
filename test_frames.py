import sys
sys.path.append("/Users/sunilkumar/Downloads/neonodes")
import neonodes.problems.bt_inorder as problem

frames = problem.run([4, 2, 6, 1, 3, 5, 7])
for idx, f in enumerate(frames[:15]):
    ft = f.get("type")
    fn = f.get("fn", "")
    locals_val = f.get("locals", {})
    node = locals_val.get("node")
    node_str = f"node_id={node.node_id} val={node.val}" if hasattr(node, "node_id") else str(node)
    print(f"Step {idx:2} | Type: {ft:12} | Fn: {fn:10} | Node: {node_str}")
