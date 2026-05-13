import string
from collections import Counter

ENGLISH_FREQ = {
    'A':0.0817,'B':0.0149,'C':0.0278,'D':0.0425,'E':0.1270,'F':0.0223,
    'G':0.0202,'H':0.0609,'I':0.0697,'J':0.0015,'K':0.0077,'L':0.0403,
    'M':0.0241,'N':0.0675,'O':0.0751,'P':0.0193,'Q':0.0010,'R':0.0599,
    'S':0.0633,'T':0.0906,'U':0.0276,'V':0.0098,'W':0.0236,'X':0.0015,
    'Y':0.0197,'Z':0.0007
}

def clean(text):
    return ''.join(c for c in text.upper() if c in string.ascii_uppercase)

def ic(text):
    text = clean(text)
    N = len(text)
    if N < 2:
        return 0.0
    freqs = Counter(text)
    return sum(f*(f-1) for f in freqs.values()) / (N*(N-1))

def estimate_period(ciphertext, max_period=15):
    ciphertext = clean(ciphertext)
    scores = {}
    for k in range(1, max_period + 1):
        groups = ['' for _ in range(k)]
        for i, ch in enumerate(ciphertext):
            groups[i % k] += ch
        avg_ic = sum(ic(g) for g in groups) / k
        scores[k] = avg_ic
    best_k = max(scores, key=scores.get)
    return best_k, scores

def chi_square(group, shift):
    N = len(group)
    if N == 0:
        return float('inf')
    decrypted = ''.join(chr((ord(c) - 65 - shift) % 26 + 65) for c in group)
    freqs = Counter(decrypted)
    score = 0.0
    for letter in string.ascii_uppercase:
        observed = freqs.get(letter, 0)
        expected = N * ENGLISH_FREQ[letter]
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score

def crack_vigenere(ciphertext, key_length):
    ciphertext = clean(ciphertext)
    groups = ['' for _ in range(key_length)]
    for i, ch in enumerate(ciphertext):
        groups[i % key_length] += ch
    
    key_shifts = []
    for idx, group in enumerate(groups):
        scores = [(s, chi_square(group, s)) for s in range(26)]
        best_shift = min(scores, key=lambda x: x[1])[0]
        key_shifts.append(best_shift)
    
    key = ''.join(chr(s + 65) for s in key_shifts)
    
    plaintext = ''
    for i, ch in enumerate(ciphertext):
        shift = key_shifts[i % key_length]
        plaintext += chr((ord(ch) - 65 - shift) % 26 + 65)
    
    return key, plaintext

if __name__ == "__main__":
    print("Shkruaj ciphertext-in (vetëm shkronja, pa hapësira):")
    user_input = input("> ")
    ciphertext = clean(user_input)
    
    if len(ciphertext) < 20:
        print("Gabim: Ciphertext-i duhet të jetë të paktën 20 shkronja për IC-në!")
    else:
        best_k, _ = estimate_period(ciphertext)
        key, plaintext = crack_vigenere(ciphertext, best_k)
        print(f"Gjatësia e çelësit: {best_k}")
        print(f"Çelësi: {key}")
        print(f"Plaintext: {plaintext}")