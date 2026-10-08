def transpose(mat: list[list[float | int]]) -> list[list]:
    res=[]
    if mat == []:
        return []
    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            raise ValueError
    for col in range(row_len):
        new_row = []
        for row in mat:
            new_row.append(row[col])
        res.append(new_row)
    return res

print('transpose')
print(f'[[1, 2, 3]] → {transpose([[1, 2, 3]])}')
print(f'[[1], [2], [3]] → {transpose([[1], [2], [3]])}')
print(f'[[1, 2], [3, 4]] → {transpose([[1, 2], [3, 4]])}')
print(f'[] → {transpose([])}')
print(f'[[1, 2], [3]] → {transpose([[1, 2], [3]])}')