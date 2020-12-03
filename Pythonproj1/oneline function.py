lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
x=[]
for i in lowercase:
    for l in lowercase:
        for j in digits:
            for k in digits:
                x.append((i+l)+j+k)
print(x)
answer=[i+l+j+k for i in lowercase for l in lowercase for j in digits for k in digits]
print(answer)