## Swift Immerse

# Installation:

## Prerequisites

- Python 3.11 or newer
- A Tuya-compatible smart bulb
- Tuya Cloud project credentials (Access ID & Access Secret)

## Clone the repository

```bash
git clone https://github.com/IbrahimCodesSwiftly/Swift-Immerse.git
cd Swift-Immerse
```

## Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure

Open the source code and replace the Tuya credentials with your own:

- Access ID
- Access Secret
- Device ID

## Run

```bash
python -m src.main
```

## Version History

### v0.2

- Configuration system using `config.json` and `defaults.json`
- Configurable capture FPS
- Smart color updates
- HSV threshold detection
- Automatic White Mode
- Automatic Black Mode

### v0.1

- Initial release
- Smart bulb control using Tuya Cloud API
- Live screen capture
- Average screen color detection
- HSV conversion
- Automatic bulb synchronization

> **Note**
> Swift Immerse currently uses the Tuya Cloud API, so your PC and smart bulb must have an active internet connection.
> Smoothing is currently intended for future Local mode.

> ⚠️ Swift Immerse is currently under active development.
> The first stable release will be v1.0.