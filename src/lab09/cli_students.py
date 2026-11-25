import argparse
import json
import sys

from src.lab08.models import format_student
from src.lab09 import group

DEFAULT_DB = "data/lab09/students.csv"


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=DEFAULT_DB, help="путь к CSV-хранилищу")

    parser = argparse.ArgumentParser(description="CRUD над students.csv")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", parents=[common], help="добавить студента")
    p.add_argument("--fio", required=True)
    p.add_argument("--birthdate", required=True)
    p.add_argument("--group", required=True)
    p.add_argument("--gpa", required=True)

    p = sub.add_parser("list", parents=[common], help="вывести список")
    p.add_argument("--sort", choices=["fio", "gpa"])

    p = sub.add_parser("find", parents=[common], help="поиск по ФИО")
    p.add_argument("--q", required=True, help="подстрока")

    p = sub.add_parser("remove", parents=[common], help="удалить по ФИО")
    p.add_argument("--fio", required=True)

    p = sub.add_parser("update", parents=[common], help="обновить запись")
    p.add_argument("--fio", required=True)
    p.add_argument("--gpa")
    p.add_argument("--group")
    p.add_argument("--birthdate")

    sub.add_parser("stats", parents=[common], help="статистика по группе")
    return parser


def run(args):
    db = args.db
    if args.cmd == "add":
        group.add_student(db, {"fio": args.fio, "birthdate": args.birthdate,
                               "group": args.group, "gpa": args.gpa})
        print("Студент добавлен")
    elif args.cmd == "list":
        for s in group.list_students(db, args.sort):
            print(format_student(s))
    elif args.cmd == "find":
        for s in group.find_students(db, args.q):
            print(format_student(s))
    elif args.cmd == "remove":
        print(f"Удалено записей: {group.remove_student(db, args.fio)}")
    elif args.cmd == "update":
        fields = {k: v for k, v in (("gpa", args.gpa), ("group", args.group),
                                    ("birthdate", args.birthdate)) if v is not None}
        if not fields:
            raise ValueError("Укажите хотя бы одно поле для обновления")
        if group.update_student(db, args.fio, **fields):
            print("Запись обновлена")
        else:
            print(f"Студент {args.fio!r} не найден", file=sys.stderr)
            return 1
    elif args.cmd == "stats":
        print(json.dumps(group.stats(db), ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (ValueError, KeyError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())