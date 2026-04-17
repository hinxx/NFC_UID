# Windows Setup

## 1. Install Python

Install Python 3.13 or newer for Windows and verify:

```bat
py --version
```

## 2. Install Reader Support

Install the ACS driver package for the `ACR122` reader.

Make sure the Windows Smart Card service is available and confirm the reader appears in Device Manager before testing.

## 3. Create a Virtual Environment

From the project folder in Command Prompt:

```bat
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

## 4. Install Project Dependencies

```bat
.\.venv\Scripts\python.exe -m pip install -e .
```

If `pyscard` fails to build, install Visual Studio Build Tools and try again.

## 5. Run the App

Read one card:

```bat
.\.venv\Scripts\python.exe -m nfc_uid read
```

Run keyboard loop mode:

```bat
.\.venv\Scripts\python.exe -m nfc_uid keyboard-loop
```

## 6. Build Windows Executables

Install the build tools:

```bat
.\.venv\Scripts\python.exe -m pip install -e ".[windows-build]"
```

Build the executables:

```bat
windows\build-windows.bat
```

Clean and rebuild:

```bat
windows\build-windows.bat clean
```

The build creates:

```text
dist\nfc-uid-console.exe
dist\nfc-uid.exe
```

Use:

- `dist\nfc-uid-console.exe` for debugging with a visible console window
- `dist\nfc-uid.exe` for normal use or Windows startup without a console window

## 7. Start at Windows Login in `keyboard-loop` Mode

The simplest setup is a shortcut in the current user's Startup folder.

1. Build the executables first.
2. Press `Win + R`.
3. Run:

```text
shell:startup
```

4. In the Startup folder, create a shortcut.
5. Set the shortcut target to the no-console executable:

```text
"C:\path\to\nfc-uid.exe" keyboard-loop --quiet --no-logging
```

6. Set `Start in` to the folder that contains `nfc-uid.exe`.
7. Sign out and back in, or restart Windows, to test it.

Recommended:

- Keep the executable in a stable location such as `C:\Apps\nfc-uid\`.
- Use `--quiet --no-logging` for startup mode so it does not print extra console output.
- If you want a visible console for troubleshooting, remove `--quiet` first.

You can also use Task Scheduler instead of the Startup folder if you want more control over delay, retries, or user session behavior.
