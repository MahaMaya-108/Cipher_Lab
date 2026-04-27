"""Caesar and Vigenere cipher implementations covering the 95-character ASCII range (32-126)."""


def encrypt_caesar(text: str, shift: int) -> str:
    return "".join(chr((ord(c) - 32 + shift) % 95 + 32) for c in text)


def decrypt_caesar(text: str, shift: int) -> str:
    return "".join(chr((ord(c) - 32 - shift) % 95 + 32) for c in text)


def encrypt_vigenere(text: str, keyword: str) -> str:
    if not keyword:
        raise ValueError("Keyword cannot be empty")
    extended_key = "".join(keyword[i % len(keyword)] for i in range(len(text)))
    return "".join(
        chr(((ord(t) - 32) + (ord(k) - 32)) % 95 + 32)
        for t, k in zip(text, extended_key)
    )


def decrypt_vigenere(text: str, keyword: str) -> str:
    if not keyword:
        raise ValueError("Keyword cannot be empty")
    extended_key = "".join(keyword[i % len(keyword)] for i in range(len(text)))
    return "".join(
        chr(((ord(t) - 32) - (ord(k) - 32)) % 95 + 32)
        for t, k in zip(text, extended_key)
    )
