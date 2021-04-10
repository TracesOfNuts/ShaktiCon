import binascii

with open("chall.png","rb") as f:
    s = f.read().hex()

new = s[:96] + s[130:]
for i in range(5):
    print(new[32*i:32*i+32])

result = binascii.a2b_hex(new)

with open("new.png","wb") as f:
    f.write(result)