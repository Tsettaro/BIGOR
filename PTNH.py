from pywebcopy import save_website
import re
from bs4 import BeautifulSoup
import requests
import os
dr = os.getcwd()
dr = dr.replace('\\','/')
source = dr+"/App/my_site/bigor.bmstu.ru/"
pages = []

def find(tag, cl):
    links = soup.find_all(tag, class_ = cl)
    for i in links:
        pages.append('http://bigor.bmstu.ru'+i.get('href'))

def root_path(text):
	x = os.path.abspath(os.sep)
	x = x.replace('\\','/')
	if text == x:
		return text+'/App/'
	else:
		return text

def fix_links(page):
    page = page.replace('/?cnt/?doc=OP2/', source+'cnt__doc_OP2_')
    page = page.replace('/?cou=OP2/OP_T','__cou_OP2_OP_T')
    page = page.replace('.cou','.cou.html\"')
    page = page.replace('gif.gif', 'gif')
    page = page.replace('/?asr/',source+'asr_')
    page = page.replace('./1557202953', source+'cnt__doc_OP2_OP_T.cou.html\"')
    return page

print("Loading main page...")

url = 'http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

find('a', 'eLModul')
find('a', 'eExtern')
find('a', 'eLTestMod')
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

files = [f for f in os.listdir(source) if f.endswith('.gif.gif')]
for i in range(len(files)):
    files[i] = files[i].replace('gif.gif', 'gif')
    if (os.path.isfile(source+files[i]) == 0):
        os.rename(source+files[i]+'.gif', source+files[i])

files = [f for f in os.listdir(source) if f.endswith('.html')]
for i in files:
    HTMLFile = open(source+i, "r")
    soup = BeautifulSoup(HTMLFile.read(), 'lxml')
    page = soup.prettify()
    page = fix_links(page)
    with open(source+i, 'w', encoding="utf-8") as file:
        file.write(page)
    HTMLFile.close()
#if (os.path.exists(source+'index.html') == 0):
#    os.rename(source+'cnt__doc_OP2_OP_T.cou.html',source+'index.html')
#os.remove(source+"index.html")

print("Now you can open BIGOR. Open file edit.html to start. Good luck!")
os.system("pause")