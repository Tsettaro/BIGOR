import sys
import matrix, time
from pywebcopy import save_website
from bs4 import BeautifulSoup
import os, shutil as sh, requests, platform
from pathlib import Path

if (platform.system() != "Windows" and platform.system() != "Linux"):
    print(f"I'm sorry, but I can't work in {platform.system()}. Please, contact to my developer for further information!")
    quit()
pages = []

def find(cl, soup):
    links = soup.find_all('a', class_ = cl)
    for i in links:
        pages.append('http://bigor.bmstu.ru'+i.get('href'))

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
            matrix.matrix()
            return ''
        case _:
            while (os.path.exists(dr) == False or (os.access(dr, os.X_OK) == False)):
                cls()
                dr = input("Please, choose the another path: ")

    if dr[-1] != '/': dr+='/'
    return dr

def setup(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    find('eLModul', soup)
    find('eExtern', soup)
    find('eLTestMod', soup)

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

def fix_links(page):
    page = page.replace('/?cnt/?doc=OP2/', source+'cnt__doc_OP2_').replace('doc=OP2/','doc_OP2_')
    page = page.replace('/?cou=OP2/OP_T','__cou_OP2_OP_T')
    page = page.replace('.cou','.cou.html\"').replace('.mod_','.mod__').replace('___','__')
    page = page.replace('gif.gif', 'gif').replace('/?frm/','/').replace('.png', '')
    page = page.replace('/?asr/',source+'asr_').replace('/?img/', '/').replace('/?','_').replace('img_','')
    page = page.replace('./1557202953', source+'cnt__doc_OP2_OP_T.cou.html\"').replace('__n_','__n=').replace('.mod_n=','.mod__n=').replace('frm_','').replace('__k_', '_k=')
    return page

print("Loading pages...")
setup('http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou')
setup('http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_P.cou')
time.sleep(2.5)
print("Links to pages added.")
time.sleep(2.5)
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

print(f"Now you can open BIGOR. Open file edit.html in \"{dr}BIGOR_stable\" to start. Good luck!")
match platform.system():
    case "Windows":
        os.system("pause")
        os.startfile(f"{dr}BIGOR_stable")
    case "Linux":
        os.system("read -n1 -r -p \"Press any key to continue...\" key")
