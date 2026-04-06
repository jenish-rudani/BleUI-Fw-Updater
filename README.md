# BleuIO Firmware Updater

A command-line tool for updating BleuIO firmware images.

## Requirements

- Python >= 3.5
- [pyserial 3.5](https://pypi.org/project/pyserial/)
- [uv](https://docs.astral.sh/uv/) (recommended)

---

## Setup with uv

### 1. Install uv (if not already installed)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone / download the project, then install dependencies

```bash
cd bleuio_fw_updater
uv sync
```

This creates a `.venv` and installs `pyserial==3.5` automatically.

---

## Usage

```bash
# Basic usage
uv run python bleuio_fw_updater.py bleuio.2.7.9.70-release.img

# With debug output
uv run python bleuio_fw_updater.py bleuio.2.7.9.70-release.img -dbg
uv run python bleuio_fw_updater.py bleuio.2.7.9.70-release.img --debug
```

### If installed as a script (via `uv tool install .`)

```bash
bleuio-fw-updater bleuio.2.7.9.70-release.img
bleuio-fw-updater bleuio.2.7.9.70-release.img --debug
```

---

## Arguments

| Argument | Description |
|---|---|
| `<firmware.img>` | Path to the firmware image file (required) |
| `-dbg` / `--debug` | Show full exception tracebacks |

---

## Project Structure

```
bleuio_fw_updater/
├── pyproject.toml        # uv / PEP 517 project metadata
├── .python-version       # Pinned Python version for uv
├── bleuio_fw_updater.py  # Main script
└── README.md
```
