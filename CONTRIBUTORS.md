# 👥 Contributors

Thank you for your interest in contributing to **lastcode**! Below is a list of the contributors who have built and maintained this project, along with instructions on how you can get involved.

---

## ✍️ Project Creator & Maintainer

* **Sunil Kumar** ([@sunil-kumarr](https://github.com/sunil-kumarr)) — Creator, lead developer, and architect of lastcode.

---

## 🤝 How to Contribute

We welcome contributions of all kinds! Whether you want to add new algorithm visualizers, fix bugs, improve the styling, or write documentation, here is how you can get started:

### 1. File an Issue
If you find a bug or want to suggest a new feature, please open an issue first to discuss it.

### 2. Fork and Clone
Fork the repository to your own GitHub account and clone it locally:
```bash
git clone https://github.com/your-username/lastcode.git
cd lastcode
```

### 3. Setup Development Environment
We use `textual` for the UI and `dev.py` for hot-reloading:
```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run hot-reloading dev watcher
python dev.py
```

### 4. Create a Feature Branch
Create a branch for your work:
```bash
git checkout -b feature/my-cool-algorithm
```

### 5. Follow the Guidelines
* Keep code style aligned with existing renderers.
* For new tree/grid problems, make sure to add hooks in the problem files (`explain_frame`, `VARIABLES`, etc.) rather than hardcoding problem logic in the renderer files.
* Test your changes inside the TUI app before making a pull request.

### 6. Submit a Pull Request
Push your branch to your fork and submit a PR to the main repository.

---

*Thank you to everyone who helps make lastcode a better learning resource for developers!*
