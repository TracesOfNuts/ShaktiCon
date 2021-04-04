import sys
from PIL import Image

myList = []
for i in range(1,3001):
    temp = './60x50/'+str(i)+'.jpg'
    myList.append(temp)

print(myList[:10])
images = [Image.open(x) for x in myList]

# each image size is 10x10
max_width = 10*50
max_height = 10*60

new_img = Image.new('RGB', (max_width, max_height))

x_offset, y_offset = 0, 0

for i in images:
  new_img.paste(i, (x_offset,y_offset))
  x_offset += 10
  if y_offset==max_height:
      break
  if x_offset==max_width:
      x_offset=0
      y_offset+=10
      continue  

new_img.save('flag.jpg')