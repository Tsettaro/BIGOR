from pywebcopy import save_website
import re
from bs4 import BeautifulSoup
import requests
import os
dr = os.getcwd()
dr = dr.replace('\\','/')
pages = []

def root_path(text):
	x = os.path.abspath(os.sep)
	x = x.replace('\\','/')
	if text == x:
		return text+'/App/'
	else:
		return text

print("Loading main page...")

url = 'http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

links = soup.find_all('a', class_ = 'eLModul')
for i in links:
    pages.append('http://bigor.bmstu.ru'+i.get('href'))
links = soup.find_all('a', class_ = 'eExtern')
for i in links:
    pages.append('http://bigor.bmstu.ru'+i.get('href'))
print("Links to pages added.")

if (os.path.exists(root_path(dr)) == 0):
    os.chdir(dr)
    os.mkdir('App')

print("Download pages...")

save_website(
    url="http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou",
    project_folder=dr+'/App/',
    project_name="my_site",
    bypass_robots=True,
    debug=False,
    open_in_browser=False,
    delay=None,
    threaded=False,
    )
for i in pages:
    save_website(
    url=i,
    project_folder=dr+'/App/',
    project_name="my_site",
    bypass_robots=True,
    debug=False,
    open_in_browser=False,
    delay=None,
    threaded=False,
    )

print("Pages successfully downloaded!")

source = dr+"/App/my_site/bigor.bmstu.ru/"
#if (os.path.exists(source+'index.html') == 0):
#    os.rename(source+'cnt__doc_OP2_OP_T.cou.html',source+'index.html')
files = [f for f in os.listdir(source) if f.endswith('.gif.gif')]
for i in range(len(files)):
    files[i] = files[i].replace('gif.gif', 'gif')
    os.rename(source+files[i]+'.gif', source+files[i])

files = [f for f in os.listdir(source) if f.endswith('.html')]
for i in files:
    HTMLFile = open(source+i, "r")
    soup = BeautifulSoup(HTMLFile.read(), 'lxml')
    page = soup.prettify()
    page = page.replace('/?cnt/?doc=OP2/', source+'cnt__doc_OP2_')
    page = page.replace('/?cou=OP2/OP_T.cou','__cou_OP2_OP_T.cou.html')
    page = page.replace('cnt__doc_OP2_OP_T.cou','cnt__doc_OP2_OP_T.cou.html')
    page = page.replace('gif.gif', 'gif')
    with open(source+i, 'w', encoding="utf-8") as file:
        file.write(page)
    HTMLFile.close()
#os.remove(source+"index.html")

print("Now you can open BIGOR. Open file edit.html to start. Good luck!")
os.system("pause")