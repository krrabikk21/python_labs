def format_record(rec: tuple[str, str, float]) -> str:
    if type(rec) != tuple:
        raise TypeError("Не кортеж")

    if len(rec) != 3:
        raise ValueError('В кортеже должно быть 3 элемента')

    fio, group, gpa = rec
    if type(fio) != str or type(group)!=str:
        raise TypeError("Фио или группа не строки")

    if type(gpa)!= float and type(gpa)!=int:
        raise TypeError('gpa не число')
    
    if gpa<0.0 or gpa> 5.0:
        raise ValueError('gpa должны быть от 0.0 до 5.0')

    fio = " ".join(fio.split())
    group = group.strip()

    if len(fio)==0 or len(group)==0:
        raise ValueError("Фио или группа пусты")

    parts = fio.split()

    if len(parts) < 2 or len(parts) > 3:
        raise ValueError('Фио должно содержать 2 или 3 слова')

    surname= parts[0].capitalize()
    newfio=''
    newfio+= surname + ' '
    for init in parts[1:]:
        newfio += init[0].upper() + '.'
    return f'{newfio}, гр. {group}, GPA {gpa:.2f}' 

print(f'("Иванов Иван Иванович", "BIVT-25", 4.6) → {format_record(("Иванов Иван Иванович", "BIVT-25", 4.6))}')
print(f'("Петров Пётр", "IKBO-12", 5.0) → {format_record(("Петров Пётр", "IKBO-12", 5.0))}')
print(f'("Петров Пётр Петрович", "IKBO-12", 5.0) → {format_record(("Петров Пётр Петрович", "IKBO-12", 5.0))}')
print(f'("  сидорова  анна   сергеевна ", "ABB-01", 3.999) → {format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999))}')