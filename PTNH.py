import sys
import scr
from pywebcopy import save_website
from bs4 import BeautifulSoup
import os, shutil as sh, requests, platform
from pathlib import Path

pages = []

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def inp():
    dr = input("Hello! And welcome to BIGOR downloader. Choose the path, where we install BIGOR: ")
    match dr:
        case '':
            match platform.system():
                case "Windows":
                    dr = os.path.expanduser('~/Documents/').replace('\\','/')
                case "Linux":
                    dr = os.path.expanduser('~/')
        case 'matrix':
            scr.matrix()
            return ''
        case _:
            while (os.path.exists(dr) == False or (os.access(dr, os.X_OK) == False)):
                cls()
                dr = input("Please, choose the another path: ")

    if dr[-1] != '/': dr+='/'
    return dr

def download(psr, link):
    r = requests.get(link) 
    soup = BeautifulSoup(r.text, 'lxml')
    images = soup.select('img')
    p = []
    for i in range(len(images)):
        p.append(images[i]['src'])
    for i in p:
        if i.endswith('.gif'):
            continue
        img = "http://bigor.bmstu.ru" + i
        name = i.replace('/','_').replace('?','_').replace('=','_',1).replace('mod_','mod__').replace('___','__').replace('__k=','_k=')
        with open(psr+name[6:], 'wb') as handler:
            img_data = requests.get(img).content 
            handler.write(img_data)

def save(link, folder):
    save_website(
    url=link,
    project_folder=dr+folder,
    project_name="my_site",
    bypass_robots=True,
    debug=False,
    open_in_browser=False,
    delay=None,
    threaded=False,
    )
    download(dr+folder+"my_site/bigor.bmstu.ru/", link)

def sort(tag, source):
    return [f for f in os.listdir(source) if f.endswith(tag)]

def cls():
    os.system('cls' if platform.system()=='Windows' else 'clear')

def find(cl):
    links = soup.find_all('a', class_ = cl)
    for i in links:
        pages.append('http://bigor.bmstu.ru'+i.get('href'))

if (platform.system() != "Windows" and platform.system() != "Linux"):
    print(f"I'm sorry, but I can't work in {platform.system()}. Please, contact to my developer for further information!")
    quit()

dr = ''
while (dr == ''):
    dr = inp()
os.chdir(dr)
if (os.path.exists("BIGOR_stable") == False):
    os.mkdir("BIGOR_stable")
    os.chdir(dr+"BIGOR_stable")
    os.mkdir('App')
source = dr+"BIGOR_stable/App/my_site/bigor.bmstu.ru/"
os.chdir(dr)


url = 'http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

def fix_links(page):
    page = page.replace('/?cnt/?doc=OP2/', source+'cnt__doc_OP2_').replace('doc=OP2/','doc_OP2_')
    page = page.replace('/?cou=OP2/OP_T','__cou_OP2_OP_T')
    page = page.replace('.cou','.cou.html\"').replace('.mod_','.mod__').replace('___','__')
    page = page.replace('gif.gif', 'gif').replace('/?frm/','/').replace('.png', '')
    page = page.replace('/?asr/',source+'asr_').replace('/?img/', '/').replace('/?','_').replace('img_','').replace('n_','n=')
    page = page.replace('./1557202953', source+'cnt__doc_OP2_OP_T.cou.html\"')
    return page

print("Loading main page...")

find('eLModul')
find('eExtern')
find('eLTestMod')

print("Links to pages added.")
print("Download pages...")

save("http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou","BIGOR_stable/App/")
for i in pages:
    save(i, "BIGOR_stable/App/")
    for images in os.listdir(source):
        if images.endswith(".png"):
            os.remove(os.path.join(source, images))



print("Pages successfully downloaded!")
files = [f for f in os.listdir(source) if f.endswith('.gif.gif')]
for i in range(len(files)):
    files[i] = files[i].replace('gif.gif', 'gif')
    if (os.path.isfile(source+files[i]) == 0):
        os.rename(source+files[i]+'.gif', source+files[i])


for i in sort('html', source):
    HTMLFile = open(source+i, "r", encoding="utf-8")
    soup = BeautifulSoup(HTMLFile.read(), 'lxml')
    page = soup.prettify()
    page = fix_links(page)
    with open(source+i, 'w', encoding="utf-8") as file:
        file.write(page)
    HTMLFile.close()

if os.path.isfile(source + 'edit.html'):
	os.remove(source+"edit.html")
sh.copy(source+'cnt__doc_OP2_OP_T.cou.html', source+'edit.html')
sh.move(source+'edit.html', dr+"BIGOR_stable")

match platform.system():
    case "Windows":
        print(f"Now you can open BIGOR. Open file edit.html in \"{dr}BIGOR_stable\" to start. Good luck!")
    case "Linux":
        print(f"Now you can open BIGOR. Open file edit.html in \"{dr}BIGOR_stable\" to start. Good luck!")
os.startfile(f"{dr}BIGOR_stable")
os.system("pause")