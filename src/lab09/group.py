import csv
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student

HEADER = list(STUDENT_FIELDS)  # ["fio", "birthdate", "group", "gpa"]


def _prepare(d):
    """Копия записи, где gpa-строка (из CSV или CLI) переведена в float.

    student_from_dict из ЛР8 строки не конвертирует, поэтому делаем это здесь.
    """
    d = dict(d)
    g = d.get("gpa")
    if isinstance(g, str):
        try:
            d["gpa"] = float(g.strip().replace(",", "."))
        except ValueError:
            raise ValueError(f"gpa: ожидается число, получено {g!r}")
    return d


# ---------------------------------------------------------------- хранилище

def ensure_storage(path):
    """Создать каталоги и файл с заголовком, если файла ещё нет."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADER)


def load_students(path):
    """Прочитать все записи; каждая строка -> student_from_dict (с валидацией)."""
    ensure_storage(path)
    with Path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or list(reader.fieldnames) != HEADER:
            raise ValueError(
                f"Неверный или отсутствующий заголовок CSV, ожидается: {','.join(HEADER)}"
            )
        students = []
        for line_no, row in enumerate(reader, start=2):
            if None in row or None in row.values():
                raise ValueError(f"Строка {line_no}: неверное число колонок")
            try:
                students.append(student_from_dict(_prepare(row)))
            except ValueError as e:
                raise ValueError(f"Строка {line_no}: {e}")
    return students


def save_students(path, students):
    """Перезаписать файл целиком."""
    ensure_storage(path)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)


# ---------------------------------------------------------------- CRUD

def add_student(path, student):
    rec = student_from_dict(_prepare(student))
    validate_student(rec)
    students = load_students(path)
    # ★ запрет дубликатов
    if any(s["fio"] == rec["fio"] for s in students):
        raise ValueError(f"Студент с ФИО {rec['fio']!r} уже существует")
    students.append(rec)
    save_students(path, students)


def list_students(path, sort_by=None):
    students = load_students(path)
    if sort_by is None:
        return students
    if sort_by == "fio":
        return sorted(students, key=lambda s: s["fio"].lower())
    if sort_by == "gpa":
        # gpa уже float (load_students), сравнение числовое, не строковое
        return sorted(students, key=lambda s: s["gpa"])
    raise ValueError(
        f"Неизвестное значение sort_by: {sort_by!r} (допустимо: None, 'fio', 'gpa')"
    )


def find_students(path, substr):
    needle = substr.lower()
    return [s for s in load_students(path) if needle in s["fio"].lower()]


def remove_student(path, fio):
    students = load_students(path)
    kept = [s for s in students if s["fio"] != fio]
    removed = len(students) - len(kept)
    if removed:
        save_students(path, kept)
    return removed


def update_student(path, fio, **fields):
    for key in fields:
        if key not in HEADER:
            raise KeyError(f"Неизвестное поле: {key}")
    students = load_students(path)
    for i, s in enumerate(students):
        if s["fio"] == fio:
            updated = student_from_dict(_prepare({**s, **fields}))
            validate_student(updated)
            students[i] = updated
            save_students(path, students)
            return True
    return False


# ---------------------------------------------------------------- ★ аналитика

def stats(path):
    students = load_students(path)
    if not students:
        return {"count": 0, "min_gpa": None, "max_gpa": None,
                "avg_gpa": None, "groups": {}, "top_5_students": []}
    gpas = [s["gpa"] for s in students]
    groups = {}
    for s in students:
        groups[s["group"]] = groups.get(s["group"], 0) + 1
    top = sorted(students, key=lambda s: s["gpa"], reverse=True)[:5]
    return {
        "count": len(students),
        "min_gpa": min(gpas),
        "max_gpa": max(gpas),
        "avg_gpa": round(sum(gpas) / len(gpas), 2),
        "groups": groups,
        "top_5_students": [{"fio": s["fio"], "gpa": s["gpa"]} for s in top],
    }