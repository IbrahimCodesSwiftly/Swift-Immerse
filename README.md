## Swift Immerse v0.1

### Features
- Smart bulb control using Tuya Cloud API
- Live screen capture
- Average screen color detection
- BGR to Tuya HSV conversion
- Automatic bulb synchronization
- Graceful shutdown

### Known limitations
- Uses Tuya Cloud (higher latency)
- Uses average screen color only
- No smoothing or optimization yet


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

> **Note**
> Swift Immerse currently uses the Tuya Cloud API, so your PC and smart bulb must have an active internet connection.