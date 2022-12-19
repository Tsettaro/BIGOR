from pywebcopy import save_website
from bs4 import BeautifulSoup
import os, shutil as sh, requests, platform
from pathlib import Path

match platform.system():
    case "Windows":
        dr = os.path.expanduser('~/Documents/')
        dr = dr.replace('\\','/')
    case "Linux":
        dr = os.path.expanduser('~/')
    case _:
        print("Sorry, but I can work only on Windows or Linux!")
        quit()

os.chdir(dr)
if (os.path.exists("BIGOR_stable") == False):
    os.mkdir("BIGOR_stable")
    os.chdir(dr+"BIGOR_stable")
    os.mkdir('App')
source = dr+"BIGOR_stable/App/my_site/bigor.bmstu.ru/"
os.chdir(dr)



pages = []

def find(tag, cl):
    links = soup.find_all(tag, class_ = cl)
    for i in links:
        pages.append('http://bigor.bmstu.ru'+i.get('href'))

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

files = [f for f in os.listdir(source) if f.endswith('.html')]
for i in files:
    HTMLFile = open(source+i, "r", encoding="utf-8")
    soup = BeautifulSoup(HTMLFile.read(), 'lxml')
    page = soup.prettify()
    page = fix_links(page)
    with open(source+i, 'w', encoding="utf-8") as file:
        file.write(page)
    HTMLFile.close()

sh.copy(source+'cnt__doc_OP2_OP_T.cou.html', source+'edit.html')
sh.move(source+'edit.html', dr+"BIGOR_stable")

match platform.system():
    case "Windows":
        print("Now you can open BIGOR. Open file edit.html in \"My documents/BIGOR_stable\" to start. Good luck!")
    case "Linux":
        print("Now you can open BIGOR. Open file edit.html in \"~/BIGOR_stable\" to start. Good luck!")

os.system("pause")