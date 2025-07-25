
"""Levenshtein-based autocorrect engine"""
import bisect
from utils import levenshtein

class AutoCorrect:
    def __init__(self, dict_path: str):
        with open(dict_path, 'r', encoding='utf-8') as f:
            self.words = sorted({w.strip().lower() for w in f if w.strip()})

    def suggest(self, token: str, max_cost: int = 2, limit: int = 5):
        cands = []
        for w in self.words:
            cost = levenshtein(token, w)
            if cost <= max_cost:
                bisect.insort(cands, (cost, w))
        if cands:
            return [w for _, w in cands[:limit]]
        scored = sorted((levenshtein(token, w), w) for w in self.words)
        return [w for _, w in scored[:limit]]
