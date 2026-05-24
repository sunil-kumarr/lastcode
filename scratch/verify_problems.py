import sys
import os
import importlib

# Ensure the root folder is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lastcode.problems.registry import PROBLEM_MAP, PROBLEMS
from lastcode.app import _load_renderer

def verify_all():
    print("Verifying lastcode problems and renderers...")
    failed = 0
    passed = 0
    
    for p in PROBLEMS:
        pid = p["id"]
        avail = p["available"]
        if not avail:
            print(f"[-] {pid:<25} (Not Available/Stub)")
            continue
            
        module_path = PROBLEM_MAP.get(pid)
        if not module_path:
            print(f"[FAIL] {pid:<25} (Missing from PROBLEM_MAP)")
            failed += 1
            continue
            
        try:
            mod = importlib.import_module(module_path)
            
            # Extract default input
            input_data = getattr(mod, "DEFAULT_INPUT", None)
            if input_data is None:
                input_data = getattr(mod, "DEFAULT_GRID", None)
                
            if input_data is None:
                print(f"[FAIL] {pid:<25} (Missing DEFAULT_INPUT / DEFAULT_GRID)")
                failed += 1
                continue
                
            frames = mod.run(input_data)
            
            # Load and run renderer logic
            renderer_name = p["renderer"]
            renderer = _load_renderer(renderer_name)
            
            filtered = renderer.filter_frames(frames)
            states = renderer.compute_states(filtered, len(filtered) - 1)
            
            print(f"[PASS] {pid:<25} (Imported, Ran, and Rendered. {len(frames)} raw frames, {len(filtered)} filtered frames)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {pid:<25} ({e})")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n----------------------------------------")
    print(f"Verification completed. Passed: {passed}, Failed: {failed}")
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    verify_all()
