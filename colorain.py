from colours import *

# Core "parent" class: ColoredText
class ColoredText:
    def __init__(self, text):
        self.text = text
        self.parsed = self.parse_color()
   
    def parse_color(self):
        return self.parse_tokens('color')
   
    def raw_text(self):
        return self.parse_tokens('raw')
   
    def parse_tokens(self, replacer):
        parsed_text = self.text
        if replacer=='color':
            for key in fgtokens:
                parsed_text = parsed_text.replace(fgtokens[key], fgcodes[key])
            for key in bgtokens:
                parsed_text = parsed_text.replace(bgtokens[key], bgcodes[key])
        elif replacer == 'raw':
            for key in fgtokens:
                parsed_text = parsed_text.replace(fgtokens[key], '')
            for key in bgtokens:
                parsed_text = parsed_text.replace(bgtokens[key], '')
        return parsed_text
   
    def add_fg_color(self, color):
        self.text = f'{fgtokens[color]}{self.raw_text()}{fgtokens["none"]}'
        self.parsed = self.parse_color()
    
    def add_bg_color(self, color):
        self.text = f'{bgtokens[color]}{self.raw_text()}{fgtokens["none"]}'
        self.parsed = self.parse_color()
    
    def __repr__(self):
        return self.parsed
    
    def __add__(self, clrtxt):
        if 'str' in str(type(clrtxt)):
            return ColoredText(self.text+clrtxt)
        if 'colorain' in str(type(clrtxt)):
            return ColoredText(self.text+clrtxt.text)

# Foreground colouring: wrapper classes
class FGColor(ColoredText):
    def __init__(self, text, color):
        super().__init__(text)
        self.add_fg_color(color)

class FGYellow(FGColor):
    def __init__(self, text):
        super().__init__(text,'yellow')

class FGRed(FGColor):
    def __init__(self, text):
        super().__init__(text, 'red')

class FGGray(FGColor):
    def __init__(self, text):
        super().__init__(text, 'darkgray')

class FGCyan(FGColor):
    def __init__(self, text):
        super().__init__(text, 'cyan')

class FGOrange(FGColor):
    def __init__(self, text):
        super().__init__(text, 'orange')

class FGGreen(FGColor):
    def __init__(self, text):
        super().__init__(text, 'green')

class FGPurple(FGColor):
    def __init__(self, text):
        super().__init__(text, 'purple')

class FGLtRed(FGColor):
    def __init__(self, text):
        super().__init__(text, 'lightred')

class FGLtGreen(FGColor):
    def __init__(self, text):
        super().__init__(text, 'lightgreen')

class FGLtCyan(FGColor):
    def __init__(self, text):
        super().__init__(text, 'lightcyan')

class FGLtPurple(FGColor):
    def __init__(self, text):
        super().__init__(text, 'lightpurple')

class FGLtBlue(FGColor):
    def __init__(self, text):
        super().__init__(text, 'lightblue')

# Background colouring: wrapper classes
class BGColor(ColoredText):
    def __init__(self, text, color):
        super().__init__(text)
        self.add_bg_color(color)

class BGYellow(BGColor):
    def __init__(self, text):
        super().__init__(text, 'yellow')

class BGRed(BGColor):
    def __init__(self, text):
        super().__init__(text, 'red')

class BGGreen(BGColor):
    def __init__(self, text):
        super().__init__(text, 'green')

class BGGray(BGColor):
    def __init__(self, text):
        super().__init__(text, 'darkgray')

class BGCyan(BGColor):
    def __init__(self, text):
        super().__init__(text, 'cyan')

class BGBlue(BGColor):
    def __init__(self, text):
        super().__init__(text, 'blue')

class BGPurple(BGColor):
    def __init__(self, text):
        super().__init__(text, 'purple')