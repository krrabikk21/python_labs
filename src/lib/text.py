import re
from collections import Counter
 
 
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    text = text.casefold() if casefold else text.lower()
    if yo2e:
        text = text.replace("ё", "е")
    # управляющие символы и пробелы -> один пробел
    return re.sub(r"[\s\x00-\x1f\x7f-\x9f]+", " ", text).strip()

# print('normalize')
# print(f'ПрИвЕт\nМИр\t→ {normalize("ПрИвЕт\nМИр\t")}')
# print(f'"ёжик, Ёлка"→ {normalize("ёжик, Ёлка")}')
# print(f'"Hello\r\nWorld"→ {normalize("Hello\r\nWorld")}')
# print(f'"  двойные   пробелы  "→ {normalize("  двойные   пробелы  ")}')

def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+(?:-\w+)*", text)

# print('tokenize')
# print(f'"привет мир" → {tokenize("привет мир")}')
# print(f'"hello,world!!!" → {tokenize("hello,world!!!")}')
# print(f'"по-настоящему круто" → {tokenize("по-настоящему круто")}')
# print(f'"2025 год → {tokenize("2025 год")}')
# print(f'"emoji 😀 не слово" → {tokenize("emoji 😀 не слово")}')

def count_freq(tokens: list[str]) -> dict[str, int]:
    return dict(Counter(tokens))
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:max(n, 0)]


# print('count_freq + top_n')
# print(f'["a","b","a","c","b","a"] → {top_n(count_freq(["a","b","a","c","b","a"]), n=2)}')
# print(f'["bb","aa","bb","aa","cc"] → {top_n(count_freq(["bb","aa","bb","aa","cc"]), n=2)}')