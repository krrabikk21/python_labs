def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    a= -100000
    b= 100000
    if len(nums)==0:
        raise ValueError("Список пуст")
    for i in range(len(nums)):
        if nums[i]<b:
            b=nums[i]
        if nums[i]>a:
            a=nums[i]
    return b, a
# print('min_max')
# print(f'[3, -1, 5, 5, 0] → {min_max([3, -1, 5, 5, 0])}')
# print(f'[42] → {min_max([42])}')
# print(f'[-5, -2, -9] → {min_max([-5, -2, -9])}')
# print(f'[1.5, 2, 2.0, -3.1] → {min_max([1.5, 2, 2.0, -3.1])}')
# print(f'[] → {min_max([])}') 

def unique_sorted(nums: list[float | int]) -> list[float | int]:
    res = []
    for i in nums:
        if i not in res:
            res.append(i)
    for i in range(len(res)):
        for j in range(len(res)-1 -i):
            if res[j]>res[j+1]:
                res[j], res[j+1] = res[j+1], res[j]
    return res

# print('unique_sorted')
# print(unique_sorted([3, 1, 2, 1, 3]))
# print(unique_sorted([]))
# print(unique_sorted([-1, -1, 0, 2, 2]))
# print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))


def flatten(mat: list[list | tuple]) -> list:
    res=[]
    for i in mat:
        if type(i)== list or type(i)== tuple:
            for new in i:
                res.append(new)
        else:
            raise TypeError
    return res
print('flatten')
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))

