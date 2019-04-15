from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os
import pyperclip
import webbrowser

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def makeURL(command):
    baseurl = "https://explainshell.com/explain?cmd="
    commandurl = urllib.parse.quote(command, safe='')
    return baseurl + commandurl


commandArr = sys.argv
commandArr.pop(0)

fromClip = False
showUrl = False
inspect = False
browser = False

remove = []
passedFirst = False

for arg in commandArr:
    if not passedFirst and '-' in arg:
        flag = arg.replace('-', '').strip()
        if flag == 'clip':
            fromClip = True
        if flag == 'url':
            showUrl = True
        if flag == 'inspect':
            inspect = True
        if flag == 'web':
            browser = True
        remove.append(arg)
    else:
        passedFirst = True

for arg in remove:
    commandArr.remove(arg)

commandStr = ""
for arg in commandArr:
    commandStr += arg + " "

if(fromClip or len(commandArr) == 0):
    commandStr = pyperclip.paste()


url = makeURL(commandStr.strip())
raw_html = simple_get(url)

if browser:
    webbrowser.open(url)

if showUrl:
    print('\nURL: ' + url)

html = BeautifulSoup(raw_html, 'html.parser')

boxes = {}

for tag in html.findAll('pre', {"class":True}):
    if 'help-box' in tag["class"]:
        boxes[tag["id"]] = [tag.text.replace('\n', '')]


for tag in html.findAll("span", {"class":True, "helpref":True}):
    if 'command0' in tag["class"]:
        boxes[tag["helpref"]].append(tag.text)
unknownCount = 0
for tag in html.findAll("span", {"class":True}):
    if 'unknown' in tag["class"]:
        boxes[unknownCount] = ["Unknown", tag.text]
        unknownCount += 1
for tag in html.select('h4'):
    if 'missing man page' in tag.text:
        print("Missing Man Page")
        sys.exit()

if inspect:
    import code; code.interact(local=dict(globals(), **locals()))

def bordered(pad, text):
    if text == None:
        test = "Unknown"
    rows, columns = os.popen('stty size', 'r').read().split()
    effectiveCol = int(columns) - pad - 4
    n = effectiveCol
    text = '\n'.join([text[i:i+n] for i in range(0, len(text), n)])
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append(' '*pad + '│' + (s.strip() + ' ' * width)[:width] + '│')
    res.append(' '*pad + '└' + '─' * width + '┘')
    return '\n'.join(res)

# import code; code.interact(local=dict(globals(), **locals()))

print('\n')
for box in boxes.keys():
    pad = 20
    print("{:^20}{}".format(boxes[box][1], bordered(pad, boxes[box][0])))

print('\n')
