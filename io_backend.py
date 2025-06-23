import io
import subprocess
from PIL import Image

import config

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
        result = subprocess.run([
            "adb",
            "exec-out",
            "screencap",
            "-p",
        ], stdout=subprocess.PIPE, check=True)
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
        subprocess.run([
            "adb",
            "shell",
            "input",
            "tap",
            str(int(x)),
            str(int(y)),
        ], check=True)
    else:
        raise ValueError(f"Unsupported IO_MODE: {config.IO_MODE}")


click = tap

__all__ = ["screenshot", "tap", "click"]
