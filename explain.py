import sys, os, pyperclip, webbrowser, re, textwrap, math, scrape_utils
import urllib.parse, bcolors

## Constants
textMargin = 3          # Margin around text in the boxes
pad = 20                # Padding of boxes from the left
maxWidth = 150
topBottomPad = True
borderColor = bcolors.ENDC
nameColor = bcolors.OKGREEN + bcolors.BOLD

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
includeCommand = False

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
        if flag == 'v':
            includeCommand = True
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
html = scrape_utils.simple_get(url)

if browser:
    webbrowser.open(url)
    sys.exit()

if includeCommand:
    print('\nexplain "' + commandStr.strip() + '"')
if showUrl:
    print('\nURL: ' + url)

boxes = {}

# The help Boxes
for tag in html.findAll('pre', {"class":True}):
    if any('help-box' in s for s in tag["class"]):
        boxes[tag["id"]] = [tag.text.replace('\n', '')]
    if any('shell' in s for s in tag["class"]):
        boxes[tag["id"]] = [tag.text.replace('\n', '')]

# The top command layout
for tag in html.findAll("span", {"class":True, "helpref":True}):
    if any('command' in s for s in tag["class"]):
        boxes[tag["helpref"]].append(tag.text)
    if any('shell' in s for s in tag["class"]):
        boxes[tag["helpref"]].append(tag.text)
unknownCount = 0
for tag in html.findAll("span", {"class":True}):
    if any('unknown' in s for s in tag["class"]):
        boxes[unknownCount] = ["Unknown", tag.text]
        unknownCount += 1
for tag in html.select('h4'):
    if 'missing man page' in tag.text:
        print(bcolors.FAIL + "Missing Man Page" + bcolors.ENDC)
        sys.exit()

if inspect:
    import code; code.interact(local=dict(globals(), **locals()))

def bordered2(pad, text, command):
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    columns = columns if columns < maxWidth else maxWidth

    if text == None:
        text = "Unknown"
    text = re.sub('\s+', ' ', text).strip()

    effectiveCol = columns - pad - 4 - (textMargin*2)
    wrapper = textwrap.TextWrapper(width=effectiveCol)
    lines = wrapper.wrap(text=text)

    if topBottomPad:
        lines.insert(0, "")
        lines.append("")

    leftSide = []
    for i in range(0, len(lines)):
        if i == 1:
            lengthAct = len(command)
            command = nameColor + command + bcolors.ENDC
            leftPad = math.ceil(float(pad - lengthAct) / 2)
            rightPad = math.floor(float(pad - lengthAct) / 2)
            leftSide.append(" "*leftPad + command + " "*rightPad)
        else:
            leftSide.append(" " * pad)

    width = max(len(s) for s in lines)

    pipe = color(borderColor, '|')
    dash = color(borderColor, '─')
    topleft = color(borderColor, '┌')
    topright = color(borderColor, '┐')
    bottomleft = color(borderColor, '└')
    bottomright = color(borderColor, '┘')

    res = [' '*pad +topleft + dash * (width + (textMargin*2)) + topright]
    for left, right in zip(leftSide, lines):
        res.append(left + pipe + ' '*(textMargin) + (right.strip() + ' ' * (width+textMargin))[:(width+textMargin)] + pipe)
    res.append(' '*pad + bottomleft + dash * (width + (textMargin*2)) + bottomright)
    return '\n'.join(res)

def color(color, text):
    return color+text+bcolors.ENDC

print()
for box in boxes.keys():
    print(bordered2(pad, boxes[box][0], boxes[box][1]))
print()
