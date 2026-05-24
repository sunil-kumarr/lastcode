import sys
import os

# Ensure the root of neonodes workspace is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from neonodes.problems.registry import PROBLEM_MAP
import importlib

PROBLEMS_TO_TEST = [
    "bt_inorder",
    "bt_preorder",
    "bt_postorder",
    "bt_max_depth",
    "bt_path_sum",
    "bt_level_order",
    "invert_tree",
    "symmetric_tree",
    "lca_bt",
    "diameter_bt",
    "balanced_bt",
    "validate_bst",
    "kth_smallest_bst",
    "lca_bst",
    "zigzag_level_order",
    "right_side_view",
    "flatten_tree",
    "path_sum_ii",
    "sum_numbers",
    "max_path_sum"
]

def test_all():
    print("Starting validation of all 20 tree problems...\n")
    success = True
    for problem_id in PROBLEMS_TO_TEST:
        module_path = PROBLEM_MAP.get(problem_id)
        if not module_path:
            print(f"[FAIL] {problem_id} is not mapped in PROBLEM_MAP!")
            success = False
            continue
            
        try:
            mod = importlib.import_module(module_path)
        except Exception as e:
            print(f"[FAIL] Failed to import {problem_id} ({module_path}): {e}")
            success = False
            continue
            
        default_input = getattr(mod, "DEFAULT_INPUT", None)
        if default_input is None:
            print(f"[FAIL] {problem_id} is missing DEFAULT_INPUT!")
            success = False
            continue
            
        try:
            frames = mod.run(default_input)
            if not frames:
                print(f"[FAIL] {problem_id} run() returned empty frames!")
                success = False
            else:
                print(f"[OK] {problem_id:20} | Found {len(frames):3} frames | Title: {getattr(mod, 'TITLE')}")
        except Exception as e:
            print(f"[FAIL] Exception raised during {problem_id}.run(): {e}")
            import traceback
            traceback.print_exc()
            success = False

    if success:
        print("\nAll 20 tree problems passed validation successfully!")
        sys.exit(0)
    else:
        print("\nSome problems failed validation.")
        sys.exit(1)

if __name__ == "__main__":
    test_all()
