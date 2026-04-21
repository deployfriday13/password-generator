import sys

from .charset import CharSet, build_alphabet, charsets_from_flags
from .clipboard import copy_to_clipboard
from .config import load_config
from .generator import calculate_entropy, generate_passphrase, generate_password

FLAG_MAP: dict[str, str] = {
    "--no-uppercase": "uppercase",
    "--no-lowercase": "lowercase",
    "--no-digits": "digits",
    "--no-symbols": "symbols",
}


def parse_password_args(args: list[str], defaults: dict) -> tuple[int, dict[str, bool]]:
    length = defaults["length"]
    charsets = {k: defaults[k] for k in ("uppercase", "lowercase", "digits", "symbols")}

    if args and args[0].isdigit():
        length = int(args[0])

    for flag, key in FLAG_MAP.items():
        if flag in args:
            charsets[key] = False

    return length, charsets


def parse_phrase_args(args: list[str], defaults: dict) -> tuple[int, str]:
    length = defaults["length"]
    delimiter = defaults["delimiter"]

    if args and args[0].isdigit():
        length = int(args[0])

    if "--delimiter" in args:
        i = args.index("--delimiter")
        if i + 1 < len(args):
            delimiter = args[i + 1]

    return length, delimiter


def main_password():
    args: list[str] = sys.argv[1:]
    config = load_config()
    length, parsed_charsets = parse_password_args(args, config["password"])

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
    config = load_config()
    length, delimiter = parse_phrase_args(args, config["phrase"])

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
