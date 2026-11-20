"""ЛР8: сериализация записей Student в JSON и обратно (+ ★ чтение из CSV)."""

import csv
import json

from src.lab08.models import student_from_dict, student_to_dict

# Выбранная политика обработки битых записей (см. README):
#   "strict" — первая же ошибка -> ValueError с номером записи и причиной
#   "skip"   — битые записи пропускаются, в конце печатается отчёт
DEFAULT_POLICY = "strict"


def students_to_json(students, path):
    """Сохраняет список записей в JSON: массив объектов."""
    data = [student_to_dict(s) for s in students]  # заодно валидирует
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _convert_all(items, policy, source):
    """Прогоняет сырые словари через student_from_dict по выбранной политике."""
    if policy not in ("strict", "skip"):
        raise ValueError(f"неизвестная политика {policy!r}, нужна 'strict' или 'skip'")

    students = []
    skipped = []  # пары (номер записи, причина)
    for number, item in enumerate(items, start=1):
        try:
            students.append(student_from_dict(item))
        except ValueError as e:
            if policy == "strict":
                raise ValueError(f"{source}: запись №{number}: {e}") from e
            skipped.append((number, str(e)))

    if skipped:
        print(f"{source}: пропущено записей: {len(skipped)}")
        for number, reason in skipped:
            print(f"  запись №{number}: {reason}")
    return students


def students_from_json(path, policy=DEFAULT_POLICY):
    """Читает JSON-массив и превращает каждую запись в валидный Student."""
    with open(path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:  # подкласс ValueError
            raise ValueError(f"{path}: некорректный JSON: {e}") from e
    if not isinstance(data, list):
        raise ValueError(f"{path}: ожидается JSON-массив записей")
    return _convert_all(data, policy, str(path))


def students_from_csv(path, policy=DEFAULT_POLICY):
    """★ Читает записи из CSV с заголовком fio,birthdate,group,gpa.

    Из CSV все значения приходят строками, поэтому gpa приводится к float
    именно здесь, на границе чтения файла. student_from_dict остаётся
    строгим: строку вместо числа он не примет.
    """
    with open(path, encoding="utf-8", newline="") as f:
        rows = []
        for row in csv.DictReader(f):
            row = dict(row)
            raw = row.get("gpa")
            if isinstance(raw, str):
                try:
                    row["gpa"] = float(raw.replace(",", "."))
                except ValueError:
                    pass  # оставляем строку: student_from_dict сообщит причину
            rows.append(row)
    return _convert_all(rows, policy, str(path))