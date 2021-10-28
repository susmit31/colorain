# Colorain
A simple package that makes printing coloured text to the console a piece of cake.

## Installation
```
pip install colorain
```

## Usage
```python
from colorain import ColoredText
txt = ColoredText('`f|y`Okay`f|n`, workin `f|c`fine`f|n`') # parses the colour tags and colour-codes the text as needed
print(txt) # prints the coloured text
print(txt.raw_text()) # strips off the colour tags
```
![Colorain](https://github.com/susmit31/colorain/ss.png)