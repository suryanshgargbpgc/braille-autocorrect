class BrailleConverter:
    def __init__(self):
        # QWERTY to Braille dot mapping
        self.qwerty_to_dots = {
            'D': 1, 'W': 2, 'Q': 3,
            'K': 4, 'O': 5, 'P': 6
        }
        
        # Braille patterns to letters mapping
        self.braille_to_letter = {
            '1': 'a', '12': 'b', '14': 'c', '145': 'd', '15': 'e',
            '124': 'f', '1245': 'g', '125': 'h', '24': 'i', '245': 'j',
            '13': 'k', '123': 'l', '134': 'm', '1345': 'n', '135': 'o',
            '1234': 'p', '12345': 'q', '1235': 'r', '234': 's', '2345': 't',
            '136': 'u', '1236': 'v', '2456': 'w', '1346': 'x', '13456': 'y',
            '1356': 'z', '': ' '
        }
        
        # Reverse mapping
        self.letter_to_braille = {v: k for k, v in self.braille_to_letter.items()}
        
        # Number patterns (prefixed with number sign)
        self.number_patterns = {
            '1': '1', '12': '2', '14': '3', '145': '4', '15': '5',
            '124': '6', '1245': '7', '125': '8', '24': '9', '245': '0'
        }
    
    def qwerty_to_braille(self, qwerty_input):
        """Convert QWERTY input to Braille pattern."""
        if not qwerty_input:
            return ''
        
        # Handle simultaneous key presses (characters in sequence)
        dots = []
        for char in qwerty_input.upper():
            if char in self.qwerty_to_dots:
                dots.append(str(self.qwerty_to_dots[char]))
        
        # Sort dots and join
        if dots:
            return ''.join(sorted(dots))
        return ''
    
    def braille_to_text(self, braille_pattern):
        """Convert Braille pattern to text."""
        if braille_pattern in self.braille_to_letter:
            return self.braille_to_letter[braille_pattern]
        return ''
    
    def text_to_braille(self, text):
        """Convert text to Braille pattern."""
        if not text:
            return ''
        
        text = text.lower()
        if text in self.letter_to_braille:
            return self.letter_to_braille[text]
        return ''
    
    def word_to_braille_patterns(self, word):
        """Convert a word to list of Braille patterns."""
        patterns = []
        for char in word.lower():
            if char in self.letter_to_braille:
                patterns.append(self.letter_to_braille[char])
        return patterns
