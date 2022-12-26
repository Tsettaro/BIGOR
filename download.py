import requests 
from bs4 import BeautifulSoup as bs 
r = requests.get('http://bigor.bmstu.ru/?cnt/?doc=OP2/shema.mod/?cou=OP2/OP_T.cou') 
soup = bs(r.text, 'lxml')
images = soup.select('img')
p = []
for i in range(len(images)):
    p.append(images[i]['src'])
for i in p:
    if i.endswith('.gif'):
        continue
    img = "http://bigor.bmstu.ru" + i
    name = i.replace('/','_').replace('?','_')
    with open('A:\BIGOR_stable/App/'+name[6:], 'wb') as handler:
        img_data = requests.get(img).content 
        handler.write(img_data)
