# Colorain v0.0.28
Ever wondered how some people make those console programmes print in pretty colours? Well, the answer is simple: there are ANSI colour codes with which you have to tag up the text. The problem is, these codes are pretty cumbersome to remember and are not built into Python either. And so typically people write bland, all-whites console programmes. Colorain is a package that makes printing coloured text to the console a piece of cake. Using a simple markup designed just for styling text on the terminal, Colorain allows you to quickly add styles to any Python console project you might have. There's a few other packages that help you to print styled text with Python, but none with the ease of use as Colorain (well, at least to me :p).

## Installation
```
pip install colorain
```

## Usage
Using a very simple markup that kinda looks like HTML, you can easily modify the colour of different parts of some text. The following example is pretty self explanatory. The general syntax is as follows: `<f=C>Text</>` colours the foreground with colour C, i.e. the text, `<b=C>Text</>` colours the background with colour C, and `<f=C1;b=C2>Text</>` or `<b=C2;f=C1>` colours the foreground with C1 and the background with C2.
```python
from colorain import *
# parses the colour tags and colour-codes the text as needed
txt = StyledText("<f=y;b=r;B;I;U>Hello world</>") 
print(txt)
```
![screenshot-1](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-1.png)

*You can use the `styles_guide()` helper function to view all the available styles and the tags for them.*
```
styles_guide()
```
![screenshot-4](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-4.png)

The core class in colorain is the StyledText class. The constructor takes a string marked up with the colorain markup and parses that to generate styled strings. The markup is fairly similar in spirit to HTML, and so is pretty simple to remember. For styling some part of a text, tag up the beginning and end of that part by the start tag/token and the end tag/token. The end tag is always the same: </>. The start tag specifies styling properties, called props. In the above code, f=y tells colorain to colour the foreground, i.e., the text itself, with 'y' i.e. yellow. Similarly, b=r tells colorain to paint the background with red. The following props, B, I, and U, tell colorain to make the text bold, italic, and underlined. You don't have to specify the props in any specific order. The start tag must contain _at least_ one styling prop.

In case you want several differently styled texts at a stretch, you don't strictly have to put an end tag after each; you can just place the end tag at the end of all of them. However, do note the slight inconsistency that arises from this. This is due to the nature of the ANSI codes, and so it's recommended that you close each tag separately. (I might add some more error checking to the library to detect if all tags have been closed. At present, it only checks if there's _at least_ one end tag, if there is(are) start tag(s).)
```
title1 = StyledText("<f=r>c <f=o>o <f=y>l <f=g>o <f=b>r <f=gr>a <f=lr>i <f=c>n  </>")
print(title1)


title2 = StyledText("<f=r>c</> <f=o>o</> <f=y>l</> <f=g>o</> <f=b>r</> <f=gr>a</> <f=lr>i</> <f=c>n</>")
print(title2)
```
![screenshot-2](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-2.png)

By the way, any StyledText object has a couple of methods you might find useful. StyledText.parse_color() gives you the parsed output string. This is the string you might directly print using the print() function, and the output will be coloured as required. In case you want to strip the text of all styles, the StyledText.raw_text() method is what you're looking for.
```
print(title1.parse_color())
print(title1.raw_text())
```
![screenshot-3](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-3.png)