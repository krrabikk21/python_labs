n=int(input(''))
och=0
zaoch=0

for i in range(n):
    b= input('')
    b = b.split()
    if b[3]=='True':
        och+=1
    else:
         zaoch+=1
print(och, zaoch)