import string

def clean(text):
    return ''.join(c for c in text.upper() if c in string.ascii_uppercase)

def encrypt_vigenere(plaintext, key):
    plaintext = clean(plaintext)
    key = clean(key)
    
    if not key:
        return None
    
    ciphertext = ''
    key_len = len(key)
    
    for i, ch in enumerate(plaintext):
        key_char = key[i % key_len]
        p_num = ord(ch) - 65
        k_num = ord(key_char) - 65
        c_num = (p_num + k_num) % 26
        ciphertext += chr(c_num + 65)
    
    return ciphertext

if __name__ == "__main__":
    plaintext = input("\nShkruaj plaintext-in: ")
    key = input("Shkruaj çelësin (fjalë, pa hapësira): ")
    
    ciphertext = encrypt_vigenere(plaintext, key)
    
    if ciphertext:
        print(ciphertext)
    else:
        print("Gabim: Çelësi nuk mund të jetë i zbrazët!")