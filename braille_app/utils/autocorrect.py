import Levenshtein
from ..models import BrailleWord

class BrailleAutocorrect:
    def __init__(self):
        self.dictionary = self._load_dictionary()
    
    def _load_dictionary(self):
        """Load dictionary with common words and their Braille patterns."""
        # Create default dictionary if empty
        if BrailleWord.objects.count() == 0:
            self._populate_default_dictionary()
        
        return {word.braille_pattern: word.word for word in BrailleWord.objects.all()}
    
    def _populate_default_dictionary(self):
        """Populate with common English words and their Braille patterns."""
        from .braille_converter import BrailleConverter
        converter = BrailleConverter()
        
        common_words = [
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'hello', 'world',
            'computer', 'keyboard', 'mouse', 'screen', 'window', 'file', 'save',
            'open', 'close', 'help', 'about', 'search', 'find', 'replace', 'copy',
            'paste', 'cut', 'undo', 'redo', 'print', 'page', 'document', 'text'
        ]
        
        for word in common_words:
            patterns = converter.word_to_braille_patterns(word)
            if patterns:
                braille_pattern = ''.join(patterns)
                BrailleWord.objects.get_or_create(
                    word=word,
                    braille_pattern=braille_pattern,
                    defaults={'frequency': 1}
                )
    
    def get_suggestions(self, user_pattern, limit=5):
        """Get suggestions for a given Braille pattern."""
        suggestions = []
        
        # Exact match
        if user_pattern in self.dictionary:
            suggestions.append({
                'word': self.dictionary[user_pattern],
                'confidence': 1.0,
                'distance': 0
            })
        
        # Find similar patterns using Levenshtein distance
        pattern_distances = []
        for pattern, word in self.dictionary.items():
            distance = Levenshtein.distance(user_pattern, pattern)
            if distance <= max(2, len(user_pattern) // 3):  # Threshold based on input length
                pattern_distances.append((pattern, word, distance))
        
        # Sort by distance and get top suggestions
        pattern_distances.sort(key=lambda x: x[2])
        
        for pattern, word, distance in pattern_distances[:limit]:
            if distance > 0:  # Don't add exact matches again
                confidence = max(0.1, 1.0 - (distance / max(len(user_pattern), len(pattern))))
                suggestions.append({
                    'word': word,
                    'confidence': round(confidence, 2),
                    'distance': distance
                })
        
        return suggestions[:limit]
    
    def learn_from_input(self, user_pattern, selected_word):
        """Learn from user selection to improve future suggestions."""
        try:
            word_obj, created = BrailleWord.objects.get_or_create(
                word=selected_word,
                braille_pattern=user_pattern,
                defaults={'frequency': 1}
            )
            if not created:
                word_obj.frequency += 1
                word_obj.save()
            
            # Update in-memory dictionary
            self.dictionary[user_pattern] = selected_word
        except Exception as e:
            print(f"Error learning from input: {e}")
