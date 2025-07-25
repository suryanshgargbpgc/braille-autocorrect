
#!/usr/bin/env python3
import argparse
from braille import decode_braille_sequence
from autocorrect import AutoCorrect

def cli():
    ap = argparse.ArgumentParser(description='Braille autocorrect CLI')
    ap.add_argument('sequence', help='Space-separated QWERTY chords e.g. "dk d k"')
    ap.add_argument('--dict', default='dictionary.txt')
    args = ap.parse_args()

    word = decode_braille_sequence(args.sequence)
    print('Decoded:', word)
    ac = AutoCorrect(args.dict)
    print('Suggestions:', ', '.join(ac.suggest(word)))

if __name__ == '__main__':
    cli()
