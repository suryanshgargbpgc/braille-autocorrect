
from flask import Flask, request, render_template_string
from braille import decode_braille_sequence
from autocorrect import AutoCorrect

app = Flask(__name__)
ac = AutoCorrect('dictionary.txt')

PAGE = """
<!doctype html>
<title>Braille Autocorrect</title>
<h1>Braille Autocorrect Demo</h1>
<form method='post'>
  <input name='seq' style='width:400px' placeholder='dk d k'>
  <input type='submit' value='Submit'>
</form>
{% if word %}
  <p>Decoded: <b>{{word}}</b></p>
  <p>Suggestions: {{ suggestions|join(', ') }}</p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    word = suggestions = None
    if request.method == 'POST':
        seq = request.form.get('seq', '')
        word = decode_braille_sequence(seq)
        suggestions = ac.suggest(word)
    return render_template_string(PAGE, word=word, suggestions=suggestions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
