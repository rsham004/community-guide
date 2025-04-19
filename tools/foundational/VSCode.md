# 🧠 VS Code Setup Guide for AI Development

This guide helps you set up **Visual Studio Code** with all the right extensions and configurations to build, test, and scale AI-powered applications.

---

## ✅ 1. Install Visual Studio Code

### 🌐 Download:
👉 https://code.visualstudio.com/

Choose your operating system (Windows, macOS, or Linux), and follow the installation steps.  

**During installation**, enable:
- ✅ Add to PATH
- ✅ Register Code as a default editor
- ✅ "Open with Code" in context menu (Windows)

---

## 🧩 2. Install Recommended Extensions

Open the Extensions panel (📦 icon in sidebar) or press `Ctrl+Shift+X` (`Cmd+Shift+X` on Mac).

Search for and install each of these, or run this one-liner if you’ve enabled the `code` CLI:

```bash
code --install-extension ms-python.python      --install-extension ms-toolsai.jupyter      --install-extension ms-toolsai.vscode-jupyter-slideshow      --install-extension ms-azuretools.vscode-docker      --install-extension ms-vscode-remote.remote-containers      --install-extension GitHub.copilot      --install-extension GitHub.copilot-chat      --install-extension ms-vscode.pylance      --install-extension esbenp.prettier-vscode      --install-extension Gruntfuggly.todo-tree      --install-extension bierner.markdown-preview-github-styles
```

### 🔧 Extensions & Why They Matter

| Extension | Use |
|-----------|-----|
| `Python` | Adds Python language support |
| `Pylance` | Fast autocompletion, type checking |
| `Jupyter` | Run notebooks & `.ipynb` files |
| `Docker` | Visual interface for container management |
| `Remote - Containers` | Open dev environments in Docker |
| `GitHub Copilot` | AI-assisted coding |
| `Copilot Chat` | Ask questions about your code |
| `Prettier` | Auto-formatting for cleaner code |
| `Todo Tree` | Find `TODO:` and `FIXME:` across files |
| `Markdown Preview` | GitHub-style rendering for `.md` files |

---

## 🧠 3. Enable `code` in Terminal (macOS/Linux only)

In VS Code, press `Cmd+Shift+P` and search:  
**Shell Command: Install 'code' command in PATH**

Then you can open projects via terminal:
```bash
code my-folder/
```

---

## 🛠️ 4. Setup for AI Projects

1. Create your project folder locally, or clone an existing one using Git.
   *(If you haven't installed Git, see the [Git Installation Guide](../foundational_dev/Git-for-windows.md))*
2. Open the folder in VS Code:
   ```bash
   code path/to/your-project
   ```
3. Create and activate a Python virtual environment.
   *   **Using Python's built-in `venv`:**
       ```bash
       # In the VS Code terminal
       python -m venv .venv
       # Activate (Windows PowerShell):
       .venv\Scripts\Activate.ps1
       # Activate (macOS/Linux bash):
       source .venv/bin/activate
       ```
   *   **Using `uv` (Recommended):** If you followed the [uv Setup Guide](../foundational_dev/UV.md), you can initialize your project and environment with:
       ```bash
       # In the VS Code terminal (after installing uv)
       uv init
       # Or sync an existing uv project:
       uv sync
       # uv automatically manages the .venv folder
       ```
4. Open the command palette `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac) → **“Python: Select Interpreter”**
   Choose the Python interpreter located inside your project's `.venv` folder.

---

## 📦 5. Install Common AI Packages

Inside your activated virtual environment:

*   **Using `pip` (if using `venv`):**
    ```bash
    pip install openai langchain transformers pandas fastapi
    ```
*   **Using `uv` (Recommended):**
    ```bash
    uv add openai langchain transformers pandas fastapi
    ```

Optionally install data science / notebook tools:

*   **Using `pip`:**
    ```bash
    pip install jupyter matplotlib seaborn scikit-learn
    ```
*   **Using `uv`:**
    ```bash
    uv add jupyter matplotlib seaborn scikit-learn
    ```

---

## 📓 6. Use Jupyter Notebooks in VS Code

- Create a `.ipynb` file to run Jupyter cells
- OR use `# %%` in `.py` files to split code into notebook-like cells

---

## 🧪 Bonus Tips

- Add a `.env` file to store API keys securely (e.g. `OPENAI_API_KEY=...`)
- Use Copilot for boilerplate suggestions and function generation
- Use Docker + Remote Containers to isolate environments for agents or services

---

## ✅ You're Ready to Build!

You now have:
- Smart Python + Jupyter support
- AI-powered assistance (Copilot)
- Easy formatting and linting
- Notebook + terminal hybrid power
- Ready-to-run LLM and automation environments

---

Happy building! 💡 Want a `.code-workspace` template to get started? Let me know.

---
*Licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)*
*Visit [ProductFoundry.ai](https://productfoundry.ai)*
