import io
import subprocess
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

import config


class ADBError(RuntimeError):
    """Raised when adb commands fail."""
    pass

if config.IO_MODE == "desktop":
    import pyautogui
else:
    pyautogui = None


def screenshot(region=None):
    """Return a PIL image of the current screen.

    For desktop mode this delegates to ``pyautogui.screenshot``. In mobile
    mode it captures the screen using ``adb exec-out screencap`` and optionally
    crops to the given region (x, y, width, height).
    """
    if config.IO_MODE == "desktop":
        return pyautogui.screenshot(region=region)
    elif config.IO_MODE == "mobile":
        try:
            result = subprocess.run([
                "adb",
                "exec-out",
                "screencap",
                "-p",
            ], stdout=subprocess.PIPE, check=True)
        except FileNotFoundError:
            logging.error("[ADB ERROR] 'adb' command not found. Check your adb installation and connection.")
            return None
        except subprocess.CalledProcessError:
            logging.error("[ADB ERROR] Failed to capture screenshot. Ensure a device is connected and authorized.")
            return None
        img = Image.open(io.BytesIO(result.stdout))
        if region:
            x, y, w, h = region
            img = img.crop((x, y, x + w, y + h))
        return img
    else:
        raise ValueError(f"Unsupported IO_MODE: {config.IO_MODE}")


def tap(x, y):
    """Simulate a screen tap/click at the given coordinates."""
    if config.IO_MODE == "desktop":
        pyautogui.click(x, y)
    elif config.IO_MODE == "mobile":
        try:
            subprocess.run([
                "adb",
                "shell",
                "input",
                "tap",
                str(int(x)),
                str(int(y)),
            ], check=True)
        except FileNotFoundError:
            msg = "[ADB ERROR] 'adb' command not found. Check your adb installation and connection."
            logging.error(msg)
            raise ADBError(msg)
        except subprocess.CalledProcessError:
            msg = "[ADB ERROR] Failed to send tap command. Ensure a device is connected and authorized."
            logging.error(msg)
            raise ADBError(msg)
    else:
        raise ValueError(f"Unsupported IO_MODE: {config.IO_MODE}")


click = tap

def press(key: str):
    """Simulate a key press."""
    if config.IO_MODE == "desktop":
        pyautogui.press(key)
    elif config.IO_MODE == "mobile":
        if len(key) == 1 and key.isalpha():
            keyevent = f"KEYCODE_{key.upper()}"
        else:
            keyevent = str(key)
        try:
            subprocess.run([
                "adb",
                "shell",
                "input",
                "keyevent",
                keyevent,
            ], check=True)
        except FileNotFoundError:
            msg = "[ADB ERROR] 'adb' command not found. Check your adb installation and connection."
            logging.error(msg)
            raise ADBError(msg)
        except subprocess.CalledProcessError:
            msg = "[ADB ERROR] Failed to send keyevent command. Ensure a device is connected and authorized."
            logging.error(msg)
            raise ADBError(msg)
    else:
        raise ValueError(f"Unsupported IO_MODE: {config.IO_MODE}")


__all__ = ["screenshot", "tap", "click", "press", "ADBError"]
