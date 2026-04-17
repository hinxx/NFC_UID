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

## 6. Build a Windows Executable

Install the build tools:

```bat
.\.venv\Scripts\python.exe -m pip install -e ".[windows-build]"
```

Build the executable:

```bat
windows\build-windows.bat
```

Clean and rebuild:

```bat
windows\build-windows.bat clean
```

The built executable will be:

```text
dist\nfc-uid.exe
```
