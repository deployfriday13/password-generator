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


def _entropy_label(bits: float) -> str:
    if bits < 50:
        return "weak"
    if bits < 80:
        return "good"
    return "strong"


def _parse_n(args: list[str]) -> int:
    if "-n" in args:
        i = args.index("-n")
        if i + 1 < len(args) and args[i + 1].isdigit():
            return int(args[i + 1])
    return 1


def parse_password_args(args: list[str], defaults: dict) -> tuple[int, int, dict[str, bool]]:
    length = defaults["length"]
    charsets = {k: defaults[k] for k in ("uppercase", "lowercase", "digits", "symbols")}
    count = _parse_n(args)

    if args and args[0].isdigit():
        length = int(args[0])

    for flag, key in FLAG_MAP.items():
        if flag in args:
            charsets[key] = False

    return length, count, charsets


def parse_phrase_args(args: list[str], defaults: dict) -> tuple[int, int, str]:
    length = defaults["length"]
    delimiter = defaults["delimiter"]
    count = _parse_n(args)

    if args and args[0].isdigit():
        length = int(args[0])

    if "--delimiter" in args:
        i = args.index("--delimiter")
        if i + 1 < len(args):
            delimiter = args[i + 1]

    return length, count, delimiter


def main_password():
    args: list[str] = sys.argv[1:]
    config = load_config()
    length, count, parsed_charsets = parse_password_args(args, config["password"])

    charsets: set[CharSet] = charsets_from_flags(**parsed_charsets)
    alphabet: str = build_alphabet(charsets)
    entropy = calculate_entropy(len(set(alphabet)), length)

    try:
        passwords = [generate_password(alphabet, length) for _ in range(count)]
    except ValueError as e:
        print(e)
        sys.exit(1)

    no_copy = "--no-copy" in args or count > 1

    if count == 1:
        if not no_copy:
            copy_to_clipboard(passwords[0])
        print(f"PASS: {passwords[0]}")
    else:
        for i, p in enumerate(passwords, 1):
            print(f"{i:>2}. {p}")

    print(f"Entropy: {entropy:.0f} bit ({_entropy_label(entropy)})")


def main_phrase():
    args: list[str] = sys.argv[1:]
    config = load_config()
    length, count, delimiter = parse_phrase_args(args, config["phrase"])
    entropy = calculate_entropy(7776, length)

    try:
        passwords = [generate_passphrase(length=length, separator=delimiter) for _ in range(count)]
    except ValueError as e:
        print(e)
        sys.exit(1)

    no_copy = "--no-copy" in args or count > 1

    if count == 1:
        if not no_copy:
            copy_to_clipboard(passwords[0])
        print(f"PASS: {passwords[0]}")
    else:
        for i, p in enumerate(passwords, 1):
            print(f"{i:>2}. {p}")

    print(f"Entropy: {entropy:.0f} bit ({_entropy_label(entropy)})")


if __name__ == "__main__":
    main_password()
