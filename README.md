# Colorain v0.0.19
Ever wondered how people make those console programmes print in pretty colours? Well, the answer is simple: there are colour codes with which you have to tag up the text. The problem is, the codes are pretty complicated, and so typically people write bland, all-whites console programmes. Colorain is a package that makes printing coloured text to the console a piece of cake. Using a simple markup designed just for colouring text on the terminal, Colorain allows you to quickly add colours to any Python project you might have. There's a few other packages that help you to print colourful text with Python, but none with the ease of use as Colorain.

## Installation
```
pip install colorain
```

## Usage
Using a very simple markup that kinda looks like HTML, you can easily modify the colour of different parts of some text. The following example is pretty self explanatory. The general syntax is as follows: `<f=C>Text</>` colours the foreground with colour C, i.e. the text, `<b=C>Text</>` colours the background with colour C, and `<f=C1;b=C2>Text</>` or `<b=C2;f=C1>` colours the foreground with C1 and the background with C2.
```python
from colorain import *
# parses the colour tags and colour-codes the text as needed
txt = ColoredText('<f=y>Okay</>, workin <f=y;b=r>fine</>') 

# prints the coloured text
print(txt) 

# strips off the colour tags and gives the raw text
print(txt.raw_text()) 

# we've overloaded the plus operator for you
# so that you can manipulate your strings just
# as usual
print(txt + FGRed("\nOr is it?") + "\n*VSauce background intensifies*")
```

![Colorain](https://github.com/susmit31/colorain/blob/master/ss.png)