import io
import subprocess
from PIL import Image

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
            print("[ADB ERROR] 'adb' command not found. Check your adb installation and connection.")
            return None
        except subprocess.CalledProcessError:
            print("[ADB ERROR] Failed to capture screenshot. Ensure a device is connected and authorized.")
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
            print(msg)
            raise ADBError(msg)
        except subprocess.CalledProcessError:
            msg = "[ADB ERROR] Failed to send tap command. Ensure a device is connected and authorized."
            print(msg)
            raise ADBError(msg)
    else:
        raise ValueError(f"Unsupported IO_MODE: {config.IO_MODE}")


click = tap

__all__ = ["screenshot", "tap", "click", "ADBError"]
