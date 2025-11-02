def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for elem in plaintext:
        order = ord(elem) + shift
        if 65 <= ord(elem) <= 90:
            if order > 90:
                order = 64 + (order % 90)
            ciphertext += chr(order)
        elif 97 <= ord(elem) <= 122:
            if order > 122:
                order = 96 + (order % 122)
            ciphertext += chr(order)
        else:
            ciphertext += elem

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    for elem in ciphertext:
        order = ord(elem) - shift
        if 65 <= ord(elem) <= 90:
            if order < 65:
                order = 91 - (65 - order)
            plaintext += chr(order)
        elif 97 <= ord(elem) <= 122:
            if order < 97:
                order = 123 - (97 - order)
            plaintext += chr(order)
        else:
            plaintext += elem

    return plaintext
