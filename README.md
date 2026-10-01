# Swift Immerse

Swift Immerse samples the average color of your primary display and uses it to control a Tuya-compatible smart bulb. It can control the bulb over your local network or through Tuya Cloud.

The project is under active development; setup and behavior may change.

## Features

- Captures and downsizes the primary display to 640 × 360 before calculating its average color.
- Sends color updates to a compatible bulb.
- Detects white and black screen content and switches the bulb mode accordingly.
- Smooths color changes using a configurable interpolation factor.
- Offers Local and Cloud Tuya backends.
- Writes detailed runtime logs to `logs/YYYY-MM-DD.log`.
- Prevents multiple copies of the app from running at the same time.

## Requirements

- Windows 10 or newer.
- Python 3.11 or newer.
- A Tuya-compatible smart bulb.
- For **Local** mode: the bulb's Device ID, local IP address, and Local Key. The PC and bulb should be on the same local network.
- For **Cloud** mode: a Tuya IoT Cloud project with Access ID, Access Secret, Device ID, and the correct regional API endpoint. An internet connection is required.

## Install

Clone the repository and open its folder:

```powershell
git clone https://github.com/IbrahimCodesSwiftly/Swift-Immerse.git
cd Swift-Immerse
```

Create a virtual environment(recommended):

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configure

1. Copy `config/defaults.json` to `config/config.json`.
2. Open `config/config.json` and select a backend with `mode`: `local` or `cloud`.
3. Fill in the Tuya values required by that backend:
   - **Local:** `DEVICE_ID`, `IP`, and `LOCAL_KEY`.
   - **Cloud:** `ACCESS_ID`, `ACCESS_SECRET`, `DEVICE_ID`, and `ENDPOINT`.
4. Adjust `capture.fps`, the HSV change thresholds, or `smoothing.factor` if needed.

`config/config.json` is ignored by Git. To keep Tuya credentials and Local Key private.

The main settings are:

| Setting | Purpose |
| --- | --- |
| `mode` | Selects the `local` or `cloud` backend. |
| `tuya` | Tuya account, device, and connection settings. |
| `capture.fps` | Screen sampling rate in frames per second. |
| `hsv.h_threshold`, `s_threshold`, `v_threshold` | Minimum HSV changes that update the target color. |
| `smoothing.factor` | Interpolation amount from 0 to 1; 1 follows the target immediately. |

The white-mode entry and exit thresholds are currently defined in `src/colors.py`.

## Run

Run the app from the project folder:

```powershell
python -m src.main
```

Press **Ctrl+C** to stop. Runtime logs are saved under `logs/`, one file per day.

## Troubleshooting

- **“Swift Immerse is already running.”** Close the other running copy, then try again.
- **Local connection errors:** Check the Device ID, IP address, Local Key, protocol version, and that the bulb and PC are on the same network.
- **Cloud connection errors:** Check the Tuya credentials, device access, internet connection, and regional API endpoint.
- **Need help diagnosing a run?** Share the relevant day's log from `logs/`. Avoid sharing `config/config.json`, which contains private credentials.
