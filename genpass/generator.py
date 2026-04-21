from math import log2
from pathlib import Path
from secrets import choice


def generate_password(alphabet: str, length: int = 15) -> str:
    if length <= 0:
        raise ValueError("The password must be at least 1 character long")
    
    password = "".join(choice(alphabet) for _ in range(length))

    return password


def generate_passphrase(
    wordlist_path: Path = Path(__file__).parent / "wordlist.txt",
    length: int = 5,
    separator: str = "-",
) -> str:
    if length <= 0:
        raise ValueError("The passphrase must be at least 1 word long")

    wordlist = load_wordlist(wordlist_path)
    password = separator.join(choice(wordlist) for _ in range(length))

    return password


def calculate_entropy(alphabet_or_words: int, length: int) -> float:
    return length * log2(alphabet_or_words)


def load_wordlist(path: Path) -> list[str]:
    with open(path, "r") as file:
        wordlist = file.read().splitlines()

    return wordlist
