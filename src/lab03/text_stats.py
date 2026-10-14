import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.text import normalize, tokenize, count_freq, top_n

sys.stdin.reconfigure(encoding="utf-8")

text = sys.stdin.read()
ntext=normalize(text)
words=tokenize(ntext)
freq= count_freq(words)
top=top_n(freq, n=5)

print(f'Всего слов: {len(words)}')
print(f'Уникальных слов: {len(freq)}')
print('Топ-5:')
for word, count in top:
    print(f'{word}:{count}')