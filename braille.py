
"""Braille mappings and decoding utilities"""
# Mapping lowercase letters a-z to their braille dot sets
BRAILLE_MAP = {
    'a': {1}, 'b': {1, 2}, 'c': {1, 4}, 'd': {1, 4, 5}, 'e': {1, 5},
    'f': {1, 2, 4}, 'g': {1, 2, 4, 5}, 'h': {1, 2, 5}, 'i': {2, 4},
    'j': {2, 4, 5}, 'k': {1, 3}, 'l': {1, 2, 3}, 'm': {1, 3, 4},
    'n': {1, 3, 4, 5}, 'o': {1, 3, 5}, 'p': {1, 2, 3, 4},
    'q': {1, 2, 3, 4, 5}, 'r': {1, 2, 3, 5}, 's': {2, 3, 4},
    't': {2, 3, 4, 5}, 'u': {1, 3, 6}, 'v': {1, 2, 3, 6},
    'w': {2, 4, 5, 6}, 'x': {1, 3, 4, 6}, 'y': {1, 3, 4, 5, 6},
    'z': {1, 3, 5, 6},
}

# QWERTY six-key mapping according to Thinkerbell spec
QWERTY_TO_DOT = {
    'D': 1, 'd': 1,
    'W': 2, 'w': 2,
    'Q': 3, 'q': 3,
    'K': 4, 'k': 4,
    'O': 5, 'o': 5,
    'P': 6, 'p': 6,
}

DOTS_TO_LETTER = {tuple(sorted(v)): k for k, v in BRAILLE_MAP.items()}

def chord_to_dots(chord: str):
    """Convert chord like 'dk' into sorted tuple of dot numbers."""
    dots = [QWERTY_TO_DOT[c] for c in chord if c in QWERTY_TO_DOT]
    return tuple(sorted(set(dots)))

def decode_braille_sequence(seq: str):
    """Decode space-separated chords into a word."""
    letters = []
    for tok in seq.split():
        letters.append(DOTS_TO_LETTER.get(chord_to_dots(tok), '?'))
    return ''.join(letters)
