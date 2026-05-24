# 🌌 neonodes

> A sleek, terminal-based interactive visualizer for tree, graph, grid, and array algorithms. Built with Python and the [Textual](https://github.com/Textualize/textual) framework.

`neonodes` allows you to trace, step-through, and animate classic coding interview problems directly in your terminal with beautiful ANSI visuals, real-time variable inspection, a code stepper, and step-by-step explanations.

---

## ✨ Features
<img width="1230" height="644" alt="image" src="https://github.com/user-attachments/assets/565bbfe4-b06d-492d-8eb4-22b455f7fe2e" />
<img width="1240" height="752" alt="image" src="https://github.com/user-attachments/assets/4fdf0410-5308-4935-b036-157e77861031" />
<img width="1282" height="854" alt="image" src="https://github.com/user-attachments/assets/7ec60df0-b88c-407e-ba15-c09b7d5fcf62" />


* **Interactive ASCII Renderers**: Visualized trees, grids, and arrays respond dynamically as the algorithm executes.
* **Trace-Driven Replay**: Leverages Python's execution tracing (`sys.settrace`) to record and reconstruct step-by-step algorithm states.
* **Variable Inspector & Legend Panel**: Keeps track of current variables, recursions, pointers, and color-coded state transitions.
* **Integrated Code Stepper**: Highlights the exact line of Python code running at each step of execution.
* **Custom Input Support**: Modify tree structures, grid dimensions, and array contents live in the application using standard format notation.
* **Hot-Reloading Dev Runner**: Active development watcher watches `.py` and `.css` files and restarts the TUI instantly on change.

---

## 🎨 Color Palette & Themes
The visualizer runs a sleek, modern Tokyonight-inspired aesthetic:
* 🌌 **Background**: `#252836` & `#1E2230`
* ⚡ **Accent Blue**: `#7AA2F7`
* 🌿 **Success Green**: `#9ECE6A`
* 🔸 **Warning/Pointer Yellow**: `#E0AF68`
* 🌹 **Critical/Path Red**: `#F7768E`

---

## 🚀 Getting Started

### Prerequisites
* **Python**: `>=3.11`
* **Package Manager**: `pip` (or [uv](https://github.com/astral-sh/uv) for lightning-fast installation)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/neonodes.git
   cd neonodes
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

---

## 🕹️ Usage

### Run the Visualizer
Start the application from anywhere using the installed shortcut:
```bash
neonodes
```
Or run the module directly:
```bash
python -m neonodes
```

### Hot-Reloading for Development
If you are modifying code, stylesheets, or adding new problems, run the watcher script. It will instantly reload the application in the terminal when changes are saved:
```bash
python dev.py
```

---

## 🎮 Keybindings & Controls

### 🏠 Home / Menu Screen
| Key | Action |
| :--- | :--- |
| `↑` / `↓` | Navigate the problem list |
| `t` | Cycle topic filters (*tree, grid, graph, array, string, dp*) |
| `d` | Cycle difficulty filters (*easy, medium, hard*) |
| `Enter` | Launch the selected visualizer |
| `q` | Quit application |

### 🛠️ Visualizer Screen
| Key | Action |
| :--- | :--- |
| `→` / `l` | **Step Forward** to the next execution frame |
| `←` / `h` | **Step Backward** to the previous execution frame |
| `Space` | **Play / Pause** auto-playback animation |
| `i` | **Edit Input** (Focuses input field to provide custom data structures) |
| `Enter` | **Submit** custom input (Parses, validates, and runs the visualizer on your input) |
| `Escape` | **Home / Cancel** input edit and return to main menu |
| `q` | **Quit** application |

---

## 🎛️ Custom Input Formats

You can press `i` on any visualization screen to customize the input. Values are parsed securely using Python's `ast.literal_eval`.

### 🌳 Binary Trees
Binary trees are represented using level-order lists.
* **Simple Binary Tree**: `[1, 2, 3, None, 4]` (representing a tree with root `1`, children `2` and `3`, and leaf `4` on the right of `2`).
* **Path-Sum Tree Problems**: `([1, 2, 3], 4)` (a tuple containing the tree array and target integer).
* *Note: Maximum tree size supported is 31 nodes.*

### 🗺️ Grids (Count Islands)
Grids are parsed as 2D lists of `0`s (water) and `1`s (land).
* **Format**: `[[1, 1, 0], [0, 1, 0], [1, 0, 1]]` (all rows must have equal width).

### 🔢 Arrays & Strings
* **Two Sum**: `[2, 7, 11, 15], 9` (the array part, followed by a comma and target sum).
* **Valid Parentheses**: `(){}[]` (a simple string of bracket characters).

---

## 📂 Project Structure

```text
neonodes/
├── dev.py                    # Hot-reloading watcher script
├── pyproject.toml            # Project dependencies and script endpoints
├── neonodes/
│   ├── main.py               # Main entrypoint
│   ├── app.py                # Main visualizer screens and layout controllers
│   ├── home.py               # Home screen widgetry and filters
│   ├── recorder.py           # Core logic tracer (tracks call frames and values)
│   ├── theme.py              # Central design-system colors
│   ├── problems/             # Interactive problems repository
│   │   ├── registry.py       # Problem metadata & path registration
│   │   ├── bt_inorder.py     # Binary Tree Inorder Traversal
│   │   ├── count_islands.py  # Count Islands
│   │   └── ... (20+ algorithm modules)
│   ├── renderers/            # UI renderers
│   │   ├── base.py           # Renderer protocol definitions
│   │   ├── tree.py           # Tree structure layout & animation renderer
│   │   ├── grid.py           # 2D Grid DFS/BFS layout renderer
│   │   └── array.py          # 1D Array tracker & stack renderer
│   └── widgets/              # Reusable textual widgets
│       └── ...               # Scrubber bars, Legend keys, variable drawers
```

---

## 📝 License
This project is licensed under the MIT License.
