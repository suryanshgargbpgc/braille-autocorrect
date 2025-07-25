
"""Utility algorithms"""
def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            ins = prev[j] + 1
            delete = curr[j-1] + 1
            sub = prev[j-1] + (ca != cb)
            curr.append(min(ins, delete, sub))
        prev = curr
    return prev[-1]
