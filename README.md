# Explain CLI

A cli interface for [ExplainShell](<https://explainshell.com/>). Scrapes and parses the responses.

***Disclaimer***: *I have only tested it on MacOS 10.14.3, and by tested, I mean it works in my environment. There is probably more setup requried than I've described.*

### Installation

**Dependencies**: (I don't know, there might be more)

- python
- requests
- beutifulsoup4
- pyperclip



**Building**

*Requires pyinstall*

```
cd Explain-CLI/
pyinstaller --onefile explain.py
```

The executable should be in `./dist/`.

### Usage

Basic usage: `explain [OPTIONS] [COMMAND]`

If no command is supplied, then it defaults to the clipboard.

Options:

- `-c, --clipboard` : Gets the command from the clipboard.
- `-url`: Prints the URL of the explainshell.com page as well.
- `-b, --browser`: Opens the explainshell.com page in a browser.
- `-echo`: Include the command in the output.

Other Notes:

- If the command includes shell operators such as '|' or '&&', then you need to wrap it in quotes.
  - e.g. `explain "cat example.txt | pbcopy"`

### Examples

**Simplest:**

```
$ ./explain "echo 'Hello World'"


      echo(1)       ┌──────────────────────┐
                    │display a line of text│
                    └──────────────────────┘
   'Hello World'    ┌──────────────────────────────────────┐
                    │Echo the STRING(s) to standard output.│
                    └──────────────────────────────────────┘
```

**No Quotes**

```
$ ./explain cat text.txt


       cat(1)       ┌──────────────────────────────────────────────────┐
                    │concatenate files and print on the standard output│
                    └──────────────────────────────────────────────────┘
      text.txt      ┌────────────────────────────────────────────────────────┐
                    │Concatenate FILE(s), or standard input, to standard outp│
                    │ut.With no FILE, or when FILE is -, read standard input.│
                    └────────────────────────────────────────────────────────┘
```



**Unknown Commands**

```
$ ./explain "say hellohoomans"


       say(1)       ┌────────────────────────────────────────────────────────┐
                    │convert text to audible speech using the GNUstep speech │
                    │engine                                                  │
                    └────────────────────────────────────────────────────────┘
    hellohoomans    ┌───────┐
                    │Unknown│
                    └───────┘
```



```
$ ./explain "hellohoomans said dogo"
Missing Man Page
```



![](http://ian.ruh.io/explain.png)

### ToDo

- [ ] Refactor Code
  - [ ] ArgParse
  - [ ] TextFormatter
- [ ] Pip package
- [ ] !! handling
- [ ]
