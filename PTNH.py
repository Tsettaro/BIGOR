from pywebcopy import save_website
from bs4 import BeautifulSoup
import os, shutil as sh, requests, platform
from pathlib import Path

pages = []

def cls():
    os.system('cls' if platform.system()=='Windows' else 'clear')

def find(tag, cl):
    links = soup.find_all(tag, class_ = cl)
    for i in links:
        pages.append('http://bigor.bmstu.ru'+i.get('href'))

if (platform.system() != "Windows" and platform.system() != "Linux"):
    print(f"I'm sorry, but I can't work in {platform.system()}. Please, contact to my developer for further information!")
    quit()
dr = input("Hello! And welcome to BIGOR downloader. Choose the path, where we install BIGOR: ")
if (dr == ''):
    match platform.system():
        case "Windows":
            dr = os.path.expanduser('~/Documents/')
            dr = dr.replace('\\','/')
        case "Linux":
            dr = os.path.expanduser('~/')
else:
	while (os.path.exists(dr) == False or (os.access(dr, os.X_OK) == False)):
		cls()
		dr = input("Please, choose the another path: ")

if dr[-1] != '/': dr+='/'

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
    page = page.replace('/?cnt/?doc=OP2/', source+'cnt__doc_OP2_')
    page = page.replace('/?cou=OP2/OP_T','__cou_OP2_OP_T')
    page = page.replace('.cou','.cou.html\"')
    page = page.replace('gif.gif', 'gif')
    page = page.replace('/?asr/',source+'asr_')
    page = page.replace('./1557202953', source+'cnt__doc_OP2_OP_T.cou.html\"')
    return page

print("Loading main page...")

find('a', 'eLModul')
find('a', 'eExtern')
find('a', 'eLTestMod')
print("Links to pages added.")

print("Download pages...")

save_website(
    url="http://bigor.bmstu.ru/?cnt/?doc=OP2/OP_T.cou",
    project_folder=dr+"BIGOR_stable/App/",
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
    project_folder=dr+"BIGOR_stable/App/",
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


for i in [f for f in os.listdir(source) if f.endswith('.html')]:
    HTMLFile = open(source+i, "r", encoding="utf-8")
    soup = BeautifulSoup(HTMLFile.read(), 'lxml')
    page = soup.prettify()
    page = fix_links(page)
    with open(source+i, 'w', encoding="utf-8") as file:
        file.write(page)
    HTMLFile.close()

sh.copy(source+'cnt__doc_OP2_OP_T.cou.html', source+'edit.html')
if os.path.isfile(source + 'edit.html'):
	os.remove(dr+"BIGOR_stable/edit.html")
sh.move(source+'edit.html', dr+"BIGOR_stable")

match platform.system():
    case "Windows":
        print(f"Now you can open BIGOR. Open file edit.html in \"{dr}BIGOR_stable\" to start. Good luck!")
    case "Linux":
        print(f"Now you can open BIGOR. Open file edit.html in \"{dr}BIGOR_stable\" to start. Good luck!")
os.startfile(f"{dr}BIGOR_stable")
os.system("pause")