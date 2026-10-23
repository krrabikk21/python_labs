import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает текстовый файл и возвращает его содержимое одной строкой.

    Args:
        path: путь к файлу (строка или ``pathlib.Path``).
        encoding: кодировка файла, по умолчанию ``"utf-8"``.

    Returns:
        Содержимое файла как одна строка (для пустого файла - ``""``).

    Raises:
        FileNotFoundError: если файл не найден.
        UnicodeDecodeError: если файл нельзя декодировать в указанной
            кодировке.

    Как выбрать другую кодировку:
        передать её в аргумент ``encoding``. Например, для файла,
        сохранённого в Windows-1251::

            read_text("data/input.txt", encoding="cp1251")

        Если при чтении в UTF-8 возникает ``UnicodeDecodeError``,
        нужно прописать ``encoding="cp1251"``.
    """
    p = Path(path)
    return p.read_text(encoding=encoding)


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские директории для ``path``, если их ещё нет.

    Args:
        path: путь к файлу, для которого нужна папка.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    """Создает/перезаписывает CSV-файл с разделителем ','.
    header: заголовок. Если передан, пишется первой строкой.
    ValueError: если строки в rows имеют разную длину.
    """
    rows = list(rows)
    if rows:
        width = len(rows[0])
        for row in rows:
            if len(row) != width:
                raise ValueError("все строки rows должны иметь одинаковую длину")
    p = Path(path)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)
if __name__ == "__main__":
    txt = read_text("data/lab04/input.txt")
    print(txt)  # должен вернуть строку
    write_csv([("word","count"),("test",3)], "data/lab04/check.csv")
    print('csv создан')  # создаст CSV