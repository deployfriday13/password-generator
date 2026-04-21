import sys

from .charset import CharSet, build_alphabet, charsets_from_flags
from .clipboard import copy_to_clipboard
from .generator import calculate_entropy, generate_passphrase, generate_password

FLAG_MAP: dict[str, str] = {
    "--no-uppercase": "uppercase",
    "--no-lowercase": "lowercase",
    "--no-digits": "digits",
    "--no-symbols": "symbols",
}


def parse_password_args(args: list[str]) -> tuple[int, dict[str, bool]]:
    """Parse CLI arguments for password generation.

    The first argument is treated as length if it is a positive integer.
    Remaining arguments are matched against FLAG_MAP to disable charsets.

    Example:
        >>> parse_password_args(["20", "--no-digits"])
        (20, {"uppercase": True, "lowercase": True, "digits": False, "symbols": True})
    """
    length = 15
    charsets = {
        "uppercase": True,
        "lowercase": True,
        "digits": True,
        "symbols": True,
    }

    if args and args[0].isdigit():
        length = int(args[0])

    for flag, key in FLAG_MAP.items():
        if flag in args:
            charsets[key] = False

    return length, charsets


def parse_phrase_args(args: list[str]) -> tuple[int, str]:
    """Parse CLI arguments for passphrase generation.

    The first argument is treated as word count if it is a positive integer.
    --delimiter VALUE sets the word separator (default: "-").

    Example:
        >>> parse_phrase_args(["3", "--delimiter", "_"])
        (3, "_")
    """
    length = 6
    delimiter = "-"

    if args and args[0].isdigit():
        length = int(args[0])

    if "--delimiter" in args:
        i = args.index("--delimiter")
        if i + 1 < len(args):
            delimiter = args[i + 1]

    return length, delimiter


def main_password():
    args: list[str] = sys.argv[1:]
    length, parsed_charsets = parse_password_args(args)

    charsets: set[CharSet] = charsets_from_flags(**parsed_charsets)
    alphabet: str = build_alphabet(charsets)

    try:
        password: str = generate_password(alphabet, length)
        entropy = calculate_entropy(len(set(alphabet)), length)

        copy_to_clipboard(password)
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f"PASS: {password}")
    print(f"Entropy: {entropy:.0f} bit")


def main_phrase():
    args: list[str] = sys.argv[1:]
    length, delimiter = parse_phrase_args(args)

    try:
        password: str = generate_passphrase(length=length, separator=delimiter)
        entropy = calculate_entropy(7776, length)

        copy_to_clipboard(password)
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f"PASS: {password}")
    print(f"Entropy: {entropy:.0f} bit")


if __name__ == "__main__":
    main_password()
