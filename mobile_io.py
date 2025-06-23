import subprocess
from PIL import Image
import io


def screenshot(region=None, path=None):
    """Capture a screenshot from a connected Android device using adb.

    Parameters
    ----------
    region : tuple(int, int, int, int), optional
        (x, y, width, height) region to crop from the screenshot.
    path : str, optional
        If provided, the image is also saved to this path.

    Returns
    -------
    PIL.Image.Image
        The captured (and optionally cropped) image.
    """
    result = subprocess.run(
        ["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE, check=True
    )
    data = result.stdout.replace(b"\r\n", b"\n")
    img = Image.open(io.BytesIO(data))
    if region is not None:
        x, y, w, h = region
        img = img.crop((x, y, x + w, y + h))
    if path:
        img.save(path)
    return img


def tap(x, y):
    """Simulate a tap on the device at the given coordinates."""
    subprocess.run(["adb", "shell", "input", "tap", str(int(x)), str(int(y))], check=True)
