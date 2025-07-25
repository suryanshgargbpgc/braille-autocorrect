from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .utils.braille_converter import BrailleConverter
from .utils.autocorrect import BrailleAutocorrect
from .models import BrailleWord

def index(request):
    return render(request, 'braille_app/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def get_suggestions(request):
    try:
        data = json.loads(request.body)
        user_input = data.get('input', '').strip()
        
        if not user_input:
            return JsonResponse({'suggestions': []})
        
        converter = BrailleConverter()
        autocorrect = BrailleAutocorrect()
        
        # Convert QWERTY input to Braille pattern
        braille_pattern = converter.qwerty_to_braille(user_input)
        
        # Get suggestions
        suggestions = autocorrect.get_suggestions(braille_pattern, limit=5)
        
        return JsonResponse({
            'suggestions': suggestions,
            'braille_pattern': braille_pattern,
            'input': user_input
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def convert_text(request):
    try:
        data = json.loads(request.body)
        user_input = data.get('input', '').strip()
        
        if not user_input:
            return JsonResponse({'converted_text': ''})
        
        converter = BrailleConverter()
        autocorrect = BrailleAutocorrect()
        
        # Split input into words
        words = user_input.split()
        converted_words = []
        
        for word in words:
            braille_pattern = converter.qwerty_to_braille(word)
            suggestions = autocorrect.get_suggestions(braille_pattern, limit=1)
            
            if suggestions:
                converted_words.append(suggestions[0]['word'])
            else:
                # If no suggestions, try to convert directly
                converted_word = converter.braille_to_text(braille_pattern)
                converted_words.append(converted_word if converted_word else word)
        
        converted_text = ' '.join(converted_words)
        
        return JsonResponse({
            'converted_text': converted_text,
            'original_input': user_input
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
