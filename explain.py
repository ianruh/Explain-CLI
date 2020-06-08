#!/usr/bin/env python3
import sys, os, pyperclip, webbrowser, scrape_utils
import urllib.parse, bcolors, argparse, textbox

## Constants
textMargin = 3          # Margin around text in the boxes
pad = 20                # Padding of boxes from the left
maxWidth = 150
topBottomPad = True
borderColor = bcolors.ENDC
nameColor = bcolors.OKGREEN + bcolors.BOLD

################ Argument parser ####################

# Meta data
parser = argparse.ArgumentParser(description='Explain shell commands.')
# Command - This argument isn't actually used, as the parsing is done before
# passing it to argparse. This is here just so the documentation is provided
# in the help text.
parser.add_argument('command',
    type=str,
    nargs='*',
    default='',
    help='The command to explain. If no command is given, the the current text\
        from the clipboard is used instead.')
# Browser
parser.add_argument('--browser',
    '-b',
    dest="inBrowser",
    action='store_true',
    help='Open the relevant explainshell.com page in a browser.')
# From clipboard
parser.add_argument('--clipboard',
    '-c',
    dest="fromClipboard",
    action='store_const',
    const=True,
    default=False,
    help='Get the command from the clipboard.')
# Show url
parser.add_argument('-url',
    dest="showUrl",
    action='store_true',
    help='Echo the URL of the relevant explainshell.com page with the output')
# Show command
parser.add_argument('-echo',
    dest="echoCommand",
    action='store_true',
    help='Echo the command being explained.')

args = []
command = []
passed = False
for arg in sys.argv:
    if not '-' == arg[0] and not 'explain' in arg:
        passed = True
    if not passed and not 'explain' in arg:
        args.append(arg)
    elif not 'explain' in arg:
        command.append(arg)
# Parse the arguments
args = parser.parse_args(args=args)

# Jankily handle the optional command
args.command = ' '.join(command)
if len(args.command) == 0:
    args.fromClipboard = True
    args.command = pyperclip.paste()

# Get the html
def makeURL(command):
    baseurl = "https://explainshell.com/explain?cmd="
    commandurl = urllib.parse.quote(command, safe='')
    return baseurl + commandurl
url = makeURL(args.command)
html = scrape_utils.simple_get(url)

# import code; code.interact(local=dict(globals(), **locals()))

# Handle some of the flags
if args.inBrowser:
    webbrowser.open(url)
    sys.exit()
if args.echoCommand:
    print('\nexplain "' + args.command.strip() + '"')
if args.showUrl:
    print('\nURL: ' + url)

###################### SCRAPE #########################

boxes = []

# (id, command, text)
def boxInsert(new_el):
    # import code; code.interact(local=dict(globals(), **locals()))
    for n in range(0, len(boxes)):
        el = boxes[n]
        if new_el[0] == el[0]:
            boxes[n] = (new_el[0], el[1], new_el[1])

# The top command layout
unknownCount = 0
for tag in html.findAll("span", {"class":True}):
    if tag.get("helpref") and any('command' in s for s in tag["class"]):
        # boxes[tag["helpref"]].append(tag.text)
        boxes.append((tag["helpref"], tag.text))
    if tag.get("helpref") and any('shell' in s for s in tag["class"]):
        # boxes[tag["helpref"]].append(tag.text)
        boxes.append((tag["helpref"], tag.text))
    if any('unknown' in s for s in tag["class"]):
        # boxes[unknownCount] = ["Unknown", tag.text]
        boxes.append((unknownCount, tag.text, "Unknown"))
        unknownCount += 1

# The help Boxes
for tag in html.findAll('pre', {"class":True}):
    if any('help-box' in s for s in tag["class"]):
        boxInsert((tag["id"], tag.text.replace('\n', '')))
    if any('shell' in s for s in tag["class"]):
        boxInsert((tag["id"], tag.text.replace('\n', '')))
for tag in html.select('h4'):
    if 'missing man page' in tag.text:
        print(bcolors.FAIL + "Missing Man Page" + bcolors.ENDC)
        sys.exit()

print()
for box in boxes:
    print(textbox.TextBox.bordered(pad, box[2], box[1]))
print()
