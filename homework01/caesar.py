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

    A_code, Z_code = 65, 90
    a_code, z_code = 97, 122

    for syl in plaintext:
        if A_code <= ord(syl) <= Z_code:
            code = ord(syl) + shift
            if code > Z_code:
                code = A_code + code % Z_code - 1
            syl = chr(code)
        elif a_code <= ord(syl) <= z_code:
            code = ord(syl) + shift
            if code > z_code:
                code = a_code + code % z_code - 1
            syl = chr(code)
        ciphertext += syl

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

    A_code, Z_code = 65, 90
    a_code, z_code = 97, 122

    for syl in ciphertext:
        if A_code <= ord(syl) <= Z_code:
            code = ord(syl) - shift
            if code < A_code:
                code = Z_code - A_code % code + 1
            syl = chr(code)
        elif a_code <= ord(syl) <= z_code:
            code = ord(syl) - shift
            if code < a_code:
                code = z_code - a_code % code + 1
            syl = chr(code)
        plaintext += syl

    return plaintext
