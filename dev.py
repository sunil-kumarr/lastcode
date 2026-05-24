#!/usr/bin/env python3
"""
dev.py — hot-reloading dev runner for lastcode.
Watches the lastcode directory and restarts the TUI application on changes.
"""

import os
import sys
import time
import subprocess

def get_mtimes(directory):
    mtimes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".css")):
                path = os.path.join(root, file)
                try:
                    mtimes[path] = os.path.getmtime(path)
                except OSError:
                    pass
    return mtimes

def main():
    # Target path is lastcode subdirectory relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    watch_dir = os.path.join(base_dir, "lastcode")
    
    print(f"Watching '{watch_dir}' for changes...")
    
    mtimes = get_mtimes(watch_dir)
    proc = None
    
    # Run the application package
    cmd = [sys.executable, "-m", "lastcode"]
    
    try:
        proc = subprocess.Popen(cmd)
        while True:
            time.sleep(0.5)
            
            # If the app exited (e.g. user quit or crashed), exit watcher too
            if proc.poll() is not None:
                sys.exit(proc.returncode)
                
            current_mtimes = get_mtimes(watch_dir)
            changed = False
            for path, mtime in current_mtimes.items():
                if path not in mtimes or mtimes[path] != mtime:
                    changed = True
                    print(f"\n[dev] Change detected in {os.path.basename(path)}. Restarting...")
                    break
            
            if not changed:
                for path in mtimes:
                    if path not in current_mtimes:
                        changed = True
                        print(f"\n[dev] File deletion detected. Restarting...")
                        break
            
            if changed:
                mtimes = current_mtimes
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                # Clear screen to make reload look clean
                os.system("clear")
                proc = subprocess.Popen(cmd)
                
    except KeyboardInterrupt:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait()
        print("\nExiting watcher.")

if __name__ == "__main__":
    main()
