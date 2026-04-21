import sys
import subprocess


def copy_to_clipboard(text: str) -> None:
    encoded = text.encode()

    if sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=encoded, check=True)
    elif sys.platform == "win32":
        subprocess.run(["clip"], input=encoded, check=True)
    else:
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=encoded, check=True)
        except FileNotFoundError:
            subprocess.run(["xsel", "--clipboard", "--input"], input=encoded, check=True)
