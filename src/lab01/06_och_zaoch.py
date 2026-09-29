n=int(input('in_1: '))
och=0
zaoch=0

for i in range(n):
    b= input(f'in_{i+2}: ')
    b = b.split()
    if b[3]=='True':
        och+=1
    else:
         zaoch+=1
print('out:', och, zaoch)