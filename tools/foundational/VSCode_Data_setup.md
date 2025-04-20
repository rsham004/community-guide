# VS Code for Data and AI Projects
## A Comprehensive Guide to Setting Up and Optimizing Your Workspace

*Last Updated: 8/2/24*

---

## What You'll Learn

- How to set up VS Code workspace
- How to style and customize VS Code
- How to optimize your workspace
- How to create and work with virtual environments
- How to 2x your productivity with the interactive mode
- How to easily integrate Git into your workflow

---

## Introduction

Visual Studio Code (VS Code) is a free integrated development environment (IDE) made by Microsoft for Windows, Linux, and macOS.

**Features:**
- Supports many languages
- Debugging capabilities
- Syntax highlighting
- Intelligent code completion (IntelliSense)
- Snippets
- Code refactoring
- Embedded Git integration

**Extensibility:**
- Highly customizable through settings.
- Large marketplace with extensions for new languages, themes, debuggers, and connections to additional services.

**Productivity:** Working in VS Code can significantly enhance your efficiency.

---

## Download VS Code

Get the latest version from the official website:
👉 [https://code.visualstudio.com](https://code.visualstudio.com)

---

## Python Installation

Ensure you have Python installed. You can get it from:

- **Official Python Installer:** [python.org](https://www.python.org/). Installs Python directly. Recommended for beginners or those wanting a pure Python experience.
- **Conda:** A package and environment manager, often used in data science. Useful for managing multiple Python environments and dependencies. See also: [Python Tool Guide](./Python.md)

Choose the method that best suits your needs.

---

## Command Palette

The Command Palette is a powerful feature for accessing commands quickly.

- **Open:** `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac).
- **Usage:** Start typing the name of a command (e.g., `Python: Select Interpreter`, `Git: Clone`).
- **Benefit:** Speeds up workflow by avoiding menu navigation and memorizing shortcuts.

---

## Workspace Setup

### Folder Organization

- **Recommendation:** Create a dedicated `Repositories` (or `repos`) folder on your drive to keep projects organized. You might further divide this into `Personal` and `Work` subfolders.

### Opening a Folder

1.  **Via UI:** `File` > `Open Folder...` > Select your project directory.
2.  **Via Terminal:**
    - First, enable the `code` command: Open Command Palette (`Ctrl+Shift+P`), search for `Shell Command: Install 'code' command in PATH`, and run it.
    - Then, navigate to your project directory in the terminal and type:
      ```bash
      code .
      ```

### Using Project Templates

- Consider using GitHub project templates for consistent project initialization.

### Saving the Workspace

- Once your folder is open and configured (e.g., extensions installed, settings adjusted), save the setup as a workspace file:
  - `File` > `Save Workspace As...`
  - Choose a location (often the root of your project folder) and give it a name (e.g., `myproject.code-workspace`).
- Opening the `.code-workspace` file later will restore your window layout, settings, and open files.

---

## Virtual Environments

Isolating project dependencies is crucial.

### Creating a Virtual Environment

1.  **Open Command Palette:** `Ctrl+Shift+P` or `Cmd+Shift+P`.
2.  **Select Command:** Type and select `Python: Select Interpreter`.
3.  **Choose Creation Method:**
    - Click `+ Create Virtual Environment...`.
    - Select either `Venv` or `Conda`.
    - **`Venv`:** Choose the base Python interpreter. VS Code will create a `.venv` folder in your workspace root.
    - **`Conda`:** If Conda is installed and detected, you can create a Conda environment.
4.  **Install Dependencies (Optional):** If your project has a `requirements.txt`, VS Code might prompt you to install them. You can also do this manually in the terminal:
    ```bash
    # Make sure your virtual environment is activated
    # Using pip:
    pip install -r requirements.txt
    # Using uv (if installed, preferred):
    uv pip install -r requirements.txt
    ```

### Verifying the Environment

- After creation, ensure the correct interpreter (from your `.venv` or Conda environment) is selected.
- The active interpreter is usually shown in the bottom-right status bar of VS Code.
- You can change it anytime using `Python: Select Interpreter` from the Command Palette.

---

## Installing Extensions

Enhance VS Code's functionality with extensions.

### How to Install

1.  Open the **Extensions View** (icon on the sidebar that looks like stacked squares, or press `Ctrl+Shift+X`).
2.  Use the search bar to find extensions by name.
3.  Click on an extension to see details.
4.  Click the `Install` button.
5.  Some extensions might require a reload of VS Code.

### Recommended Extensions

- **Python Extension Pack** (`ms-python.python`, `ms-python.vscode-pylance`): Essential Python support, linting, debugging, IntelliSense.
- **GitHub Copilot** (`GitHub.copilot`, `GitHub.copilot-chat`): AI code completion and chat (Requires subscription).
- **Path Intellisense** (`christian-kohler.path-intellisense`): Autocompletes file and folder paths.
- **GitHub Pull Requests and Issues** (`GitHub.vscode-pull-request-github`): Manage PRs and issues directly within VS Code.
- **Better Comments** (`aaron-bond.better-comments`): Improve comment visibility with highlighting.
- **Ruff** (`charliermarsh.ruff`): Extremely fast Python linter and formatter.
- **Material Icon Theme** (`PKief.material-icon-theme`): Adds specific icons for different file types and folders.
- **Atom One Dark Theme** (`akamud.vscode-theme-atom-one-dark`): A popular dark theme (or choose your favorite).

---

## Styling VS Code

Customize the look and feel.

### Changing Themes

1.  Open Settings (`Ctrl+,` or `Cmd+,`).
2.  Search for `Theme`.
3.  Select `Color Theme` (e.g., `Atom One Dark`).
4.  Select `File Icon Theme` (e.g., `Material Icon Theme`).

### Customizing Folder Icons (Material Icon Theme)

1.  Open your User Settings JSON file: Command Palette (`Ctrl+Shift+P`) > `Preferences: Open User Settings (JSON)`.
2.  Add or modify the `material-icon-theme.folders.associations` section to map folder names to specific icons provided by the theme. Example:
    ```json
  "material-icon-theme.folders.associations": {
    "venv": "environment",
    "references": "docs",
    "modeling": "generator"
  },
    ```
    *(Refer to the Material Icon Theme documentation for available icon names)*

---

## Auto Formatting with Ruff

Keep your Python code clean and consistent automatically.

1.  **Enable Format on Save:**
    - Open Settings (`Ctrl+,`).
    - Search for `Format on Save`.
    - Ensure the checkbox is ticked.
2.  **Set Ruff as Default Formatter for Python:**
    - Open Settings (`Ctrl+,`).
    - Search for `Default Formatter`.
    - Select `Ruff` from the dropdown.
3.  **Configure Actions on Save (Optional but Recommended):**
    - Open your User or Workspace `settings.json` file.
    - Add the following to enable auto-fixing and import sorting on save:
      ```json
      "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.codeActionsOnSave": {
              "source.fixAll": "explicit",
              "source.organizeImports": "explicit"
          }
      }
      ```
    *(Note: `formatOnType` mentioned in the original text is generally less common and can sometimes be disruptive; `formatOnSave` is standard practice).*

---

## Running Jupyter Notebooks

VS Code provides excellent support for `.ipynb` files.

1.  Create or open a `.ipynb` file.
2.  **Select Kernel:** Use the kernel picker (usually top-right) or Command Palette (`Jupyter: Select Kernel`) to choose the Python interpreter associated with your project's virtual environment (`.venv` or Conda env).
3.  Run cells using `Shift+Enter` or the play icons.

---

## Interactive Jupyter Window (Highly Recommended)

A powerful way to run Python code interactively without the full notebook structure.

1.  **Enable Setting:**
    - Open Settings (`Ctrl+,`).
    - Search for `Send Selection To Interactive Window`.
    - Ensure the `Jupyter: Send Selection To Interactive Window` setting is checked.
2.  **Usage:**
    - Open a regular `.py` file.
    - Highlight a block of Python code.
    - Press `Shift+Enter`.
3.  **Result:** The highlighted code runs in a separate "Interactive Window" panel. This window maintains state (variables, imports) across executions, making it ideal for data exploration, testing snippets, and iterative development.

### Setting Notebook File Root (Optional)

If your notebooks are in a subdirectory (e.g., `app/` or `notebooks/`) and you want relative paths in the notebook to resolve correctly from that directory:

1.  Open your Workspace `settings.json` file (`.vscode/settings.json`).
2.  Add the `jupyter.notebookFileRoot` setting:
    ```json
    "settings": {
        "jupyter.notebookFileRoot": "${workspaceFolder}/app" // Adjust 'app' to your notebook directory
    }
    ```

---

## GitHub Integration

VS Code has built-in Git capabilities and integrates well with GitHub.

### Source Control Panel

- Access via the sidebar icon (`Ctrl+Shift+G`).
- **Stage Changes:** Click the `+` icon next to modified files.
- **Commit:** Enter a commit message in the input box and press `Ctrl+Enter` (or `Cmd+Enter`).
- **Branching:** View the current branch in the bottom-left status bar. Click it to switch or create branches.
- **Push/Pull/Sync:** Use the `...` menu in the Source Control panel or the sync icon (arrows) in the status bar.

### GitHub Pull Requests and Issues Extension

- If installed, allows you to view, manage, and comment on PRs and issues directly within VS Code.

### Copilot for Commit Messages (Optional)

- If using GitHub Copilot Chat, you can ask it to generate commit messages based on staged changes (e.g., `@workspace /git commit`).

---

You now have a well-configured VS Code environment optimized for Python, Data Science, and AI development!
