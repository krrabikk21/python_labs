def transpose(mat: list[list[float | int]]) -> list[list]:
    res=[]
    if mat == []:
        return []
    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            raise ValueError('рваная матрица')
    for col in range(row_len):
        new_row = []
        for row in mat:
            new_row.append(row[col])
        res.append(new_row)
    return res

# print('transpose')
# print(f'[[1, 2, 3]] → {transpose([[1, 2, 3]])}')
# print(f'[[1], [2], [3]] → {transpose([[1], [2], [3]])}')
# print(f'[[1, 2], [3, 4]] → {transpose([[1, 2], [3, 4]])}')
# print(f'[] → {transpose([])}')
# print(f'[[1, 2], [3]] → {transpose([[1, 2], [3]])}')

def row_sums(mat: list[list[float | int]]) -> list[float]:
    row_len = len(mat[0])
    res=[]
    for row in mat:
        if len(row) != row_len:
            raise ValueError('рваная матрица')
    for row in mat:
        res.append(sum(row))
    return res

# print('row_sums')
# print(f'[[1, 2, 3], [4, 5, 6]] → {row_sums([[1, 2, 3], [4, 5, 6]])}')
# print(f'[[-1, 1], [10, -10]] → {row_sums([[-1, 1], [10, -10]])}')
# print(f'[[0, 0], [0, 0]] → {row_sums([[0, 0], [0, 0]])}')
# print(f'[[1, 2], [3]] → {row_sums([[1, 2], [3]])}')

def col_sums(mat: list[list[float | int]]) -> list[float]:
    row_len = len(mat[0])
    res=[]
    for row in mat:
        if len(row) != row_len:
            raise ValueError('рваная матрица')
    for i in range(row_len):
        res.append(sum(row[i] for row in mat))
    return res

print('col_sums')
print(f'[[1, 2, 3], [4, 5, 6]] → {col_sums([[1, 2, 3], [4, 5, 6]])}')
print(f'[[-1, 1], [10, -10]] → {col_sums([[-1, 1], [10, -10]])}')
print(f'[[0, 0], [0, 0]] → {col_sums([[0, 0], [0, 0]])}')
print(f'[[1, 2], [3]] → {col_sums([[1, 2], [3]])}')