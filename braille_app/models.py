from django.db import models

class BrailleWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    braille_pattern = models.CharField(max_length=200)
    frequency = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.word
    
    class Meta:
        ordering = ['-frequency', 'word']
