"""ЛР8: модель Student как словарь с фиксированным набором ключей.

В модуле нет классов: запись — обычный dict, а все операции над ней —
функции. Любая функция может положиться на константу STUDENT_FIELDS.
"""

import re
from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")

# Строго YYYY-MM-DD: date.fromisoformat в Python 3.11+ принимает и другие
# ISO-форматы (например, 20030215), поэтому формат проверяем отдельно.
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------- проверки полей

def _check_text(field, value):
    """fio и group: строка, после strip() непустая."""
    if not isinstance(value, str):
        raise ValueError(
            f"{field}: ожидается строка, получено {type(value).__name__}"
        )
    if not value.strip():
        raise ValueError(f"{field}: строка не должна быть пустой")


def _check_birthdate(value):
    """birthdate: строка YYYY-MM-DD, дата существует и не в будущем."""
    if not isinstance(value, str):
        raise ValueError(
            f"birthdate: ожидается строка, получено {type(value).__name__}"
        )
    if not _DATE_RE.match(value):
        raise ValueError(
            f"birthdate: неверный формат {value!r}, ожидается YYYY-MM-DD"
        )
    try:
        born = date.fromisoformat(value)
    except ValueError as e:
        raise ValueError(f"birthdate: такой даты не существует ({value!r}): {e}")
    if born > date.today():
        raise ValueError(f"birthdate: дата {value!r} в будущем")


def _check_gpa(value):
    """gpa: int или float (не bool), 0 <= gpa <= 5."""
    # bool — подкласс int, поэтому проверяем его первым
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"gpa: ожидается число, получено {type(value).__name__} ({value!r})"
        )
    if not (0 <= value <= 5):  # для nan условие тоже ложно
        raise ValueError(f"gpa: значение {value!r} вне диапазона 0..5")


def _check_values(fio, birthdate, group, gpa):
    _check_text("fio", fio)
    _check_birthdate(birthdate)
    _check_text("group", group)
    _check_gpa(gpa)


# ---------------------------------------------------------------- основные функции

def make_student(fio, birthdate, group, gpa):
    """Функция-конструктор: проверяет каждое поле и собирает запись."""
    _check_values(fio, birthdate, group, gpa)
    return {
        "fio": fio.strip(),
        "birthdate": birthdate,
        "group": group.strip(),
        "gpa": float(gpa),
    }


def validate_student(rec):
    """Проверяет готовый словарь: набор ключей и значения.

    При любой проблеме — ValueError. Ничего не возвращает.
    """
    if not isinstance(rec, dict):
        raise ValueError(f"запись должна быть словарём, получено {type(rec).__name__}")

    keys = set(rec)
    expected = set(STUDENT_FIELDS)
    if keys != expected:
        problems = []
        missing = sorted(expected - keys)
        extra = sorted(keys - expected, key=str)
        if missing:
            problems.append(f"нет ключей: {', '.join(missing)}")
        if extra:
            problems.append(f"лишние ключи: {', '.join(map(str, extra))}")
        raise ValueError("набор ключей не совпадает с STUDENT_FIELDS — " + "; ".join(problems))

    _check_values(rec["fio"], rec["birthdate"], rec["group"], rec["gpa"])


def student_age(rec, today=None):
    """Полных лет на дату today (по умолчанию — сегодня)."""
    validate_student(rec)
    today = today or date.today()
    born = date.fromisoformat(rec["birthdate"])
    if today < born:
        raise ValueError(f"дата {today} раньше даты рождения {born}")
    # если в этом году день рождения ещё не наступил — вычитаем год
    had_birthday = (today.month, today.day) >= (born.month, born.day)
    return today.year - born.year - (0 if had_birthday else 1)


def _short_fio(fio):
    """'Иванов Иван Иванович' -> 'Иванов И.И.' (инициалы из ЛР1)."""
    parts = fio.split()
    surname, rest = parts[0], parts[1:]
    initials = "".join(p[0].upper() + "." for p in rest)
    return f"{surname} {initials}".strip()


def _years_word(n):
    """Правильная форма слова: 1 год, 2 года, 5 лет, 11 лет, 21 год."""
    if 11 <= n % 100 <= 14:
        return "лет"
    last = n % 10
    if last == 1:
        return "год"
    if 2 <= last <= 4:
        return "года"
    return "лет"


def format_student(rec):
    """Красивый вывод: Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30"""
    validate_student(rec)
    age = student_age(rec)
    return (
        f"{_short_fio(rec['fio'])} ({rec['group']}), "
        f"{age} {_years_word(age)}, GPA {rec['gpa']:.2f}"
    )


def student_to_dict(rec):
    """Копия записи для сериализации (это другой объект, а не сам rec)."""
    validate_student(rec)
    return {key: rec[key] for key in STUDENT_FIELDS}


def student_from_dict(d):
    """Десериализация: берём ровно нужные ключи, gpa -> float, валидируем.

    Лишние ключи во входном словаре игнорируются, отсутствующие — ошибка.
    """
    if not isinstance(d, dict):
        raise ValueError(f"запись должна быть объектом, получено {type(d).__name__}")
    missing = [key for key in STUDENT_FIELDS if key not in d]
    if missing:
        raise ValueError(f"нет ключей: {', '.join(missing)}")

    rec = {key: d[key] for key in STUDENT_FIELDS}
    # int -> float; bool и строки не трогаем, их отловит validate_student
    if isinstance(rec["gpa"], int) and not isinstance(rec["gpa"], bool):
        rec["gpa"] = float(rec["gpa"])
    validate_student(rec)
    return rec


# ---------------------------------------------------------------- ★ дополнительное

def update_student(rec, **fields):
    """Возвращает НОВУЮ запись с изменёнными полями; rec не меняется.

    Неизвестный ключ — KeyError, неверное значение — ValueError.
    """
    unknown = [key for key in fields if key not in STUDENT_FIELDS]
    if unknown:
        raise KeyError(f"неизвестные поля: {', '.join(unknown)}")
    new_rec = dict(rec)       # копия, чтобы не трогать исходную запись
    new_rec.update(fields)
    return student_from_dict(new_rec)  # внутри — validate_student