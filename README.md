
## 🛠 Contributing to the Documentation

Welcome! We use **MkDocs** with the **Material** theme to build our documentation. Follow these steps to set up your environment and contribute.

### 1. Prerequisites

You need **Python** installed on your system. You can check this by running:

```bash
python --version

```

### 2. Installation

First, clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Install MkDocs and the Material theme
pip install mkdocs-material

```

### 3. Local Development

To see your changes in real-time, start the built-in development server:

```bash
mkdocs serve

```

Once started, open your browser to **`http://127.0.0.1:8000`**. The page will automatically refresh whenever you save a file.

---

## 📝 How to Add or Edit Pages

MkDocs uses a simple structure: all content lives in the `docs/` folder, and the navigation is managed in `mkdocs.yml`.

### Step 1: Create the Markdown file

Add a new `.md` file inside the `docs/` directory. For example, to add a "Setup Guide":

* Path: `docs/setup-guide.md`
* Content: Use standard Markdown syntax.

### Step 2: Register the page in `mkdocs.yml`

MkDocs won't show your page in the sidebar unless you add it to the `nav` section of your configuration file.

```yaml
site_name: My Project Docs
theme:
  name: material

nav:
  - Home: index.md
  - User Guide:
      - Installation: installation.md
      - Setup Guide: setup-guide.md  # <--- Add your new page here
  - Contributing: contributing.md

```

### Step 3: Formatting Tips

* **Admonitions:** Use these for notes or warnings.
```markdown
!!! note
    This is a helpful tip for contributors.

```


* **Links:** Use relative paths to link between pages.
`Check out the [Installation Guide](installation.md).`

---

## 🚀 Submitting Your Changes

1. **Branch:** Create a new branch for your changes (`git checkout -b docs/add-setup-guide`).
2. **Lint:** Ensure there are no broken links by running `mkdocs build`.
3. **PR:** Commit your changes and open a Pull Request!

**Would you like me to create a GitHub Action script that automatically deploys these docs whenever you merge to the main branch?**
