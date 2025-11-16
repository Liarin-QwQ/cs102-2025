def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    for k, elem in enumerate(plaintext):
        if elem.isalpha():
            if 97 <= ord(elem) <= 122:
                shift = ord(keyword[k % len(keyword)]) - ord('a')
                ciphertext += chr((ord(elem) - ord('a') + shift + 26) % 26 + ord('a'))
            elif 65 <= ord(elem) <= 90:
                shift = ord(keyword[k % len(keyword)]) - ord('A')
                ciphertext += chr((ord(elem) - ord('A') + shift + 26) % 26 + ord('A'))
        else:
            ciphertext += elem
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    for k, elem in enumerate(ciphertext):
        if elem.isalpha():
            if 97 <= ord(elem) <= 122:
                shift = ord(keyword[k % len(keyword)]) - ord('a')
                plaintext += chr((ord(elem) - ord('a') - shift + 26) % 26 + ord('a'))
            elif 65 <= ord(elem) <= 90:
                shift = ord(keyword[k % len(keyword)]) - ord('A')
                plaintext += chr((ord(elem) - ord('A') - shift + 26) % 26 + ord('A'))
        else:
            plaintext += elem
    return plaintext