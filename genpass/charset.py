from enum import Enum


_VALID_CHARSET_KEYS = {"uppercase", "lowercase", "digits", "symbols"}

class CharSet(Enum):
    """Character groups available for password generation"""

    LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    SYMBOLS = "!#$%&*+-/:<=>?@^_|~"


def charsets_from_flags(**charsets) -> set[CharSet]:
    """Return the set of CharSet members enabled by the given keyword flags

    Raises:
        ValueError: If all flags are False and the result would be empty.
        KeyError: If an unexpected flag name is passed

    Example:
        >>> charsets_from_flags(uppercase=True, lowercase=True, digits=False, symbols=False)
        {CharSet.UPPERCASE_LETTERS, CharSet.LOWERCASE_LETTERS}
    """
    invalid_keys = set(charsets) - _VALID_CHARSET_KEYS

    if invalid_keys:
        raise KeyError(f"Unknown charset flags: {invalid_keys}")

    if not any((charsets.values())):
        raise ValueError("At least one charset must be included")

    mapping = {
        CharSet.UPPERCASE_LETTERS: charsets["uppercase"],
        CharSet.LOWERCASE_LETTERS: charsets["lowercase"],
        CharSet.DIGITS: charsets["digits"],
        CharSet.SYMBOLS: charsets["symbols"],
    }

    return {charset for charset, enabled in mapping.items() if enabled}


def build_alphabet(charsets: set[CharSet]) -> str:
    """Concatenate character values from the given CharSet members into a single string"""

    return "".join(c.value for c in charsets)