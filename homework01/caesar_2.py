def decrypt_growing_shift(ciphertext, start, delta):
    plaintext = ""

    for k, elem in enumerate(ciphertext):
        shift = start + (delta * k)
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
