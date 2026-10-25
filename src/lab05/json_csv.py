import csv
import json
from pathlib import Path


def _check_suffix(path: Path, suffix: str) -> None:
    """Проверяет расширение файла, иначе ValueError."""
    if path.suffix.lower() != suffix:
        raise ValueError(f"Неверный тип файла: ожидался {suffix}, получен {path.name!r}")


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.

    Порядок колонок: как в первом объекте; ключи, которых нет в первом
    объекте, добавляются в конец в порядке появления. Отсутствующие поля
    заполняются пустыми строками. Кодировка - UTF-8.

    Args:
        json_path: путь к входному ``.json`` файлу.
        csv_path: путь к выходному ``.csv`` файлу.

    Raises:
        FileNotFoundError: если JSON-файл не найден.
        ValueError: если расширение не ``.json``/``.csv``, JSON пустой
            (``[]`` или пустой файл), некорректен или не является
            списком словарей.
    """
    src, dst = Path(json_path), Path(csv_path)
    _check_suffix(src, ".json")
    _check_suffix(dst, ".csv")

    with open(src, encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    data = json.loads(text)  # JSONDecodeError - подкласс ValueError

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON-списка должны быть словарями")

    fieldnames: list[str] = []
    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV-файл в JSON (список словарей).

    Заголовок обязателен (первая строка), все значения остаются строками.
    Запись: ``json.dump(..., ensure_ascii=False, indent=2)``, UTF-8.

    Args:
        csv_path: путь к входному ``.csv`` файлу.
        json_path: путь к выходному ``.json`` файлу.

    Raises:
        FileNotFoundError: если CSV-файл не найден.
        ValueError: если расширение не ``.csv``/``.json``, CSV пустой
            (нет заголовка или нет строк данных) или в строке больше
            значений, чем в заголовке.
    """
    src, dst = Path(csv_path), Path(json_path)
    _check_suffix(src, ".csv")
    _check_suffix(dst, ".json")

    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, restval="")
        if not reader.fieldnames:
            raise ValueError("CSV-файл пуст или без заголовка")
        rows = list(reader)

    if not rows:
        raise ValueError("В CSV-файле нет строк данных")
    if any(None in row for row in rows):
        raise ValueError("В CSV есть строка с большим числом значений, чем в заголовке")

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Демонстрация (запуск из корня проекта: python -m src.lab05.json_csv)
    json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")
    print("Готово: data/out/people_from_json.csv, data/out/people_from_csv.json")