# Colorain v0.0.50
Ever wondered how some people make those console programmes print in pretty colours? Well, the answer is simple: there are ANSI colour codes with which you have to tag up the text. The problem is, these codes are pretty cumbersome to remember and are not built into Python either. And so typically people write bland, all-whites console programmes. Colorain is a package that makes printing coloured text to the console a piece of cake. Using a simple markup designed just for styling text on the terminal, Colorain allows you to quickly add styles to any Python console project you might have. There's a few other packages that help you to print styled text with Python, but none with the ease of use as Colorain (well, at least to me :p).

## Installation
```
pip install colorain
```

## Usage
Using a very simple markup that kinda looks like HTML, you can easily modify the colour of different parts of some text. The general syntax is as follows: `<f=C>Text</>` colours the foreground with colour C, i.e. the text, `<b=C>Text</>` colours the background with colour C, and `<f=C1;b=C2>Text</>` or `<b=C2;f=C1>` colours the foreground with C1 and the background with C2.

### A Hello World Example
```python
from colorain import *
# parses the colour tags and colour-codes the text as needed
txt = StyledText("<f=y;b=r;B;I;U>Hello world</>") 
print(txt)
```
![screenshot-1](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-1.png)

### Getting Help
*You can use the `styles_guide()` helper function to view all the available styles and the tags for them.*
```
styles_guide()
```
![screenshot-4](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-4.png)

### The Syntax
The core class in colorain is the StyledText class. The constructor takes a string marked up with the colorain markup and parses that to generate styled strings. The markup is fairly similar in spirit to HTML, and so is pretty simple to remember. 

For styling some part of a text, tag up the beginning and end of that part by the _start tag_ and the _end tag_. The end tag is always the same: `</>`. The start tag specifies styling properties, called _props_. In the Hello World example above, `f=y` tells colorain to colour the foreground, i.e., the text itself, with 'y' i.e. yellow. Similarly, `b=r` tells colorain to paint the background with red. The following props, `B`, `I`, and `U`, tell colorain to make the text bold, italic, and underlined. You don't have to specify the props in any specific order. The start tag must contain _at least_ one styling prop. If you're using more than one prop, make sure you separate them with semicolons.

In case you want several differently styled texts at a stretch, you don't strictly have to put an end tag after each; you can just place the end tag at the end of all of them. However, do note the slight inconsistency that arises from this. This is due to the nature of the ANSI codes, and so it's recommended that you close each tag separately. (I might add some more error checking to the library to detect if all tags have been closed. At present, it only checks if there's _at least_ one end tag, if there is(are) start tag(s).)
```
title1 = StyledText("<f=r>c <f=o>o <f=y>l <f=g>o <f=b>r <f=gr>a <f=lr>i <f=c>n  </>")
print(title1)


title2 = StyledText("<f=r>c</> <f=o>o</> <f=y>l</> <f=g>o</> <f=b>r</> <f=gr>a</> <f=lr>i</> <f=c>n</>")
print(title2)
```
![screenshot-2](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-2.png)

### Useful Features
**parse_color() and raw_text()**:
Any StyledText object has a couple of methods you might find useful. `StyledText.parse_color()` gives you the parsed output string, i.e., ANSI colour-coded string. This is the string you might directly print using the print() function, and the output will be coloured as required. This is useful, for example, if you want to copy the ANSI coded string. You could send that to any friend of yours who hasn't installed colorain and they could copy the string to directly print the styled text. In case you want to strip the text of all styles, the `StyledText.raw_text()` method is what you're looking for. (By the way, in the following snippet I'm using a third-party module called clipboard. You should check that out if you haven't already - really great for automating certain tasks!)
```
import clipboard
print(title1.parse_color())
clipboard.copy(title1.parse_color()) # copies the ANSI coded string to your clipboard
print(title1.raw_text())
clipboard.copy(title1.raw_text()) # copies an unstyled version of the string to your clipboard
```
![screenshot-3](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-3.png)

**Wrapper Classes**:
In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long stretch of text styled the same way? It might become kinda tedious to remember to put in the end tag. If that's what you're worried about, then you can use the wrapper classes built into colorain, all of which inherit from `StyledText`.
```
print(FGYellow("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.\
"""))
print(FGLtRed("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.\
"""))
print(Bold("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.\
"""))
print(Italic("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.\
"""))
```
![screenshot-5](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-5.png)

**Adding together styled strings**:
colorain overloads the `+` operator for `StyledText` objects so that you can manipulate them as you manipulate regular strings. 
```
print(FGYellow("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.
""") + FGLtRed("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.
""")+ Bold("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.
""")+ Italic("""\
    In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.\
"""))
```
![screenshot-6](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-6.png)


### Errors
If you mess something up in the markup, there's some (slightly) informative errors that might help you with debugging.
```
print(StyledText("""\
    <f=>In case you have to style short stretches of text, using the markup is very easy. However, what if you had a long
    stretch of text in the same way? It might become kinda tedious to remember to put in the end tag. If that's what 
    you're worried about, then you can use the wrapper classes built into colorain.</>\
"""))
```

![screenshot-7](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-7.png)
![screenshot-8](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-8.png)
![screenshot-9](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-9.png)
![screenshot-10](https://raw.githubusercontent.com/susmit31/colorain/master/assets/colorain-10.png)

### Lastly, the entire thing is a work in progress by an amateur coder. Please let me know if you find any errors or have any suggestions! Thank you!