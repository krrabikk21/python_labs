"""Демонстрация ЛР8. Запуск из корня репозитория: python -m src.lab08.demo"""

from datetime import date

from src.lab08.models import (
    format_student,
    make_student,
    student_age,
    update_student,
    validate_student,
)
from src.lab08.serialize import (
    students_from_csv,
    students_from_json,
    students_to_json,
)

INPUT = "data/lab08/students_input.json"
OUTPUT = "data/lab08/students_output.json"
BAD = "data/lab08/students_bad.json"
CSV = "data/lab08/students.csv"


def section(title):
    print(f"\n=== {title} ===")


def main():
    section("1. Корректные записи: JSON -> записи -> JSON")
    students = students_from_json(INPUT)
    for s in students:
        print(format_student(s))
    students_to_json(students, OUTPUT)
    again = students_from_json(OUTPUT)
    print(f"записано в {OUTPUT}, прочитано обратно: {len(again)}, "
          f"совпадает с исходным списком: {again == students}")

    section("2. student_age: день рождения 2007-09-20")
    rec = make_student("Козлова Мария Дмитриевна", "2007-09-20", "БИВТ-26-6-2", 4.55)
    print("на 2026-09-19:", student_age(rec, date(2026, 9, 19)))
    print("на 2026-09-20:", student_age(rec, date(2026, 9, 20)))

    section("3. Запись с неверной датой (2003-02-30)")
    try:
        make_student("Смирнов Олег Игоревич", "2003-02-30", "БИВТ-26-6-1", 4.0)
    except ValueError as e:
        print("ValueError:", e)

    section("4. Запись с gpa = 7")
    try:
        make_student("Орлова Екатерина Павловна", "2006-08-01", "БИВТ-26-6-2", 7)
    except ValueError as e:
        print("ValueError:", e)

    section("5. validate_student: лишний и недостающий ключ")
    for bad in (
        {"fio": "А Б В", "birthdate": "2006-01-01", "group": "Г", "gpa": 4, "email": "x"},
        {"fio": "А Б В", "birthdate": "2006-01-01", "gpa": 4},
    ):
        try:
            validate_student(bad)
        except ValueError as e:
            print("ValueError:", e)

    section("6. Битый файл, политика strict (по умолчанию)")
    try:
        students_from_json(BAD)
    except ValueError as e:
        print("ValueError:", e)

    section("7. Битый файл, политика skip")
    good = students_from_json(BAD, policy="skip")
    print("загружено валидных записей:", len(good))

    section("8. ★ update_student не меняет исходную запись")
    s1 = students[0]
    s2 = update_student(s1, gpa=4.8)
    print("s1['gpa'] =", s1["gpa"], "| s2['gpa'] =", s2["gpa"], "| один объект:", s1 is s2)
    for kwargs in ({"email": "x"}, {"gpa": 9}):
        try:
            update_student(s1, **kwargs)
        except (KeyError, ValueError) as e:
            print(f"{type(e).__name__}:", e)

    section("9. ★ students_from_csv")
    for s in students_from_csv(CSV):
        print(format_student(s), "| тип gpa:", type(s["gpa"]).__name__)


if __name__ == "__main__":
    main()