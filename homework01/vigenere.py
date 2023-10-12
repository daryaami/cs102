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

    utf_A, utf_Z = 65, 90
    utf_a, utf_z = 97, 122

    keyword = keyword.upper()
    keyword_length = len(keyword)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encode = dict(zip(alphabet, range(26)))

    for idx, syl in enumerate(plaintext):
        shift = encode[keyword[idx % keyword_length]]
        syl_utf = ord(syl)

        if utf_A <= syl_utf <= utf_Z:
            code = syl_utf + shift
            if code > utf_Z:
                code = utf_A + code % utf_Z - 1
            syl = chr(code)

        elif utf_a <= syl_utf <= utf_z:
            code = syl_utf + shift
            if code > utf_z:
                code = utf_a + code % utf_z - 1
            syl = chr(code)

        ciphertext += syl

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

    utf_A, utf_Z = 65, 90
    utf_a, utf_z = 97, 122

    keyword = keyword.upper()
    keyword_length = len(keyword)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encode = dict(zip(alphabet, range(26)))

    for idx, syl in enumerate(ciphertext):
        shift = encode[keyword[idx % keyword_length]]
        syl_utf = ord(syl)

        if utf_A <= syl_utf <= utf_Z:
            code = syl_utf - shift
            if code < utf_A:
                code = utf_Z - utf_A % code + 1
            syl = chr(code)

        elif utf_a <= syl_utf <= utf_z:
            code = syl_utf - shift
            if code < utf_a:
                code = utf_z - utf_a % code + 1
            syl = chr(code)

        plaintext += syl

    return plaintext
