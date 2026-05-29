import re


def redact(text: str, pattern: str | re.Pattern) -> tuple[str, dict[str, str]]:
    """
    Redact all regex matches in text, returning the redacted string and a
    mapping that can be passed to unredact() to restore original values.
    """
    mapping: dict[str, str] = {}
    counter = 0

    def replace(match: re.Match) -> str:
        nonlocal counter
        placeholder = f"__REDACTED_{counter}__"
        mapping[placeholder] = match.group(0)
        counter += 1
        return placeholder

    redacted_text = re.sub(pattern, replace, text)
    return redacted_text, mapping


def unredact(text: str, mapping: dict[str, str]) -> str:
    """
    Restore original values in a redacted string using the mapping from redact().
    """
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)
    return text


if __name__ == "__main__":
    prompt = (
        "Patient SSN is 123456789 and their account number is 987654321. "
        "Please do not share employee ID 456789123 with anyone outside HR. "
        "Reference code ABC-XYZ is not sensitive but 000111222 should be hidden."
    )

    pattern = r"\b\d{9}\b"

    print("Original:")
    print(prompt)
    print()

    redacted, mapping = redact(prompt, pattern)
    print("Redacted:")
    print(redacted)
    print()

    print("Mapping:")
    for placeholder, original in mapping.items():
        print(f"  {placeholder} -> {original}")
    print()

    restored = unredact(redacted, mapping)
    print("Restored:")
    print(restored)
    print()

    print("Roundtrip match:", prompt == restored)
