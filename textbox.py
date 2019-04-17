import os, re, textwrap, bcolors, math
class TextBox:
    def color(color, text):
        return color+text+bcolors.ENDC

    def bordered(pad, text, command, maxWidth=400, textMargin=3,
            topBottomPad=True, nameColor=bcolors.OKGREEN+bcolors.BOLD,
            borderColor=bcolors.ENDC):
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

        pipe = TextBox.color(borderColor, '|')
        dash = TextBox.color(borderColor, '─')
        topleft = TextBox.color(borderColor, '┌')
        topright = TextBox.color(borderColor, '┐')
        bottomleft = TextBox.color(borderColor, '└')
        bottomright = TextBox.color(borderColor, '┘')

        res = [' '*pad +topleft + dash * (width + (textMargin*2)) + topright]
        for left, right in zip(leftSide, lines):
            res.append(left + pipe + ' '*(textMargin) + (right.strip() + ' ' * (width+textMargin))[:(width+textMargin)] + pipe)
        res.append(' '*pad + bottomleft + dash * (width + (textMargin*2)) + bottomright)
        return '\n'.join(res)
