
# Braille Autocorrect and Suggestion System

Minimal proof-of-concept for six-key QWERTY Braille input with autocorrect.

## Quick CLI Test
```bash
python main.py "dk d k"   # -> cat
```

## Web Demo
```bash
pip install -r requirements.txt
python server.py
# open http://localhost:5000
```

Replace `dictionary.txt` with a larger word list for production.

braille-autocorrect/
│
├─ braille.py          # chord ⇄ Braille logic
├─ utils.py            # Levenshtein helper
├─ autocorrect.py      # suggestion engine
│
├─ main.py             # CLI entry-point
├─ server.py           # Flask web server
│
├─ dictionary.txt      # sample word list
├─ requirements.txt    # Flask (plus Gunicorn optional)
├─ README.md           # setup & deployment guide
│
└─ tests/              # pytest suites
   ├─ test_braille.py
   └─ test_autocorrect.py
