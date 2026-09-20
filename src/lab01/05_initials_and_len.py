fio = input('ФИО:')
inic=''

fio = fio.split()
for i in fio:
    inic+=i[0]
new = " ".join(fio)
print(f'Инициалы: {inic}.')
print(f'Длина (символов): {len(new)}')
