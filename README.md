# NFC_UID

Read the UID of an NFC card or tag with `pyscard`.

Current version: `0.7`

## Features

- Read one UID and return it from Python
- Loop continuously and print each scanned UID
- Type the UID via keyboard emulation
- In `keyboard-loop` mode, emit a UID once per card presentation and wait until the card is removed before emitting it again

## Requirements

- Python `>=3.7`
- A supported PC/SC NFC reader
- `pyscard`
- `keyboard` for keyboard emulation modes

Tested setup:

- Reader: `ACR122`
- OS: `Windows 10`
- Python: `3.13`

## Installation

Install from the project root:

```bash
pip install .
```

Or install the runtime dependencies directly:

```bash
pip install -r requirements.txt
```

The package metadata currently declares these runtime dependencies:

- `keyboard>=0.13.5`
- `pyscard>=2.0.2`

## Python Usage

```python
from nfc_uid.nfc_uid import NFC_UID

reader = NFC_UID()

uid = reader.read()
print(uid)
```

Read once with explicit options:

```python
from nfc_uid.nfc_uid import NFC_UID

reader = NFC_UID(logging=False)
uid = reader.read(
    output=True,
    keyboard_type=False,
    connect_timeout=30,
    max_retries=3,
    cooldown=1,
)
print(uid)
```

Run continuous keyboard output:

```python
from nfc_uid.nfc_uid import NFC_UID

reader = NFC_UID()
reader.looped_read(
    keyboard_type=True,
    connect_timeout=30,
    max_retries=None,
    cooldown=1,
)
```

### API

`NFC_UID.read(output=True, keyboard_type=False, connect_timeout=120, max_retries=8, cooldown=2)`

- `output`: print reader status and success messages
- `keyboard_type`: type the UID through the `keyboard` package instead of returning it normally
- `connect_timeout`: timeout in seconds while waiting for a card
- `max_retries`: maximum number of retry attempts, or `None` for infinite retries
- `cooldown`: delay in seconds between retry attempts

`NFC_UID.looped_read(output=True, keyboard_type=False, connect_timeout=120, max_retries=8, cooldown=2)`

- Repeats `read()` while `reader.loop` is `True`
- With `keyboard_type=True`, the same card is only emitted once until it is removed and presented again

## CLI Usage

The package exposes a console command:

```bash
nfc-uid --help
```

You can also run it directly:

```bash
python -m nfc_uid --help
```

Available modes:

- `read`: read one UID and exit
- `loop`: continuously read and print UIDs
- `keyboard`: type one UID and exit
- `keyboard-loop`: continuously type UIDs, once per card presentation

Examples:

```bash
nfc-uid read
nfc-uid loop --quiet --retries -1
nfc-uid keyboard
nfc-uid keyboard-loop --timeout 30 --cooldown 1
```

CLI options:

- `--timeout`: card detection timeout in seconds
- `--retries`: maximum retries, use `-1` for infinite retries
- `--cooldown`: delay between retries in seconds
- `--quiet`: suppress reader status messages
- `--no-logging`: disable internal logging messages

Stopping the CLI:

- Press `Ctrl+C` to stop any console mode cleanly.
- On Windows, the reader wait is polled in short intervals so `Ctrl+C` should exit promptly instead of waiting for the full `--timeout` value.

## Windows EXE

The Windows build produces two executables:

- `nfc-uid-console.exe`: console build for debugging
- `nfc-uid.exe`: no-console build for normal use and startup

See [windows/WINDOWS.md](windows/WINDOWS.md) for Windows build and startup instructions.

## Notes

- The old camelCase argument names have been removed. Use snake_case names such as `keyboard_type`, `connect_timeout`, and `max_retries`.
- `nfc_reader()` is still present for backward compatibility inside the codebase, but it is deprecated.
- If `pyscard` or `keyboard` is missing, the package raises a runtime error with the install command instead of trying to install packages automatically.
- `Ctrl+C` only applies to console runs such as `python -m nfc_uid ...` or `nfc-uid-console.exe`. The no-console Windows build cannot receive `Ctrl+C`.

## License

GNU AGPLv3
