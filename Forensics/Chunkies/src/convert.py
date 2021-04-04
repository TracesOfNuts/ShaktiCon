import binascii

with open("file.png","rb") as f:
    s = f.read().hex()

# IDAT typo locations as tuples given by (line number,offset)
idat = [(3,10), (516,2), (1028,26), (1541,18), (2054,10), (2567,2)]
index = []
for i in idat:
    temp = 32*(i[0]-1)+i[1]
    index.append(temp)
#print(index)
new =   '89'   + s[:index[0]] +             \
        '4441' + s[index[0]+4:index[1]] +   \
        '4441' + s[index[1]+4:index[2]] +   \
        '4441' + s[index[2]+4:index[3]] +   \
        '4441' + s[index[3]+4:index[4]] +   \
        '4441' + s[index[4]+4:index[5]] +   \
        '4441' + s[index[5]+4:-16] +        \
        '49454e44ae426082'


#new = '89' + s[:74] + '4441' + s[78:-16] + '49454e44ae426082'
#print(new[:10], new[-20:])
print(new[70:82])
result = binascii.a2b_hex(new)

with open("new.png","wb") as f:
    f.write(result)