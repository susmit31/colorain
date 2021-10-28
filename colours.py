BASE_CLR = {
    'black':0,
    'red':1,
    'green':2,
    'yellow':3,
    'blue':4,
    'purple':5,
    'cyan':6,
    'gray':7
}

GROUND = {'BG':4, 'FG':3} # Background prefix


def gcode(ground):
    return lambda clr: f"{GROUND[ground]}{BASE_CLR[clr]}"

class Color:
    def __init__(self, GROUND):
        code = gcode(GROUND)
        self.black = f"0;{code('black')}"
        self.red = f'0;{code("red")}'
        self.green = f"0;{code('green')}"
        self.orange = f'0;{code("yellow")}'
        self.blue = f'0;{code("blue")}'
        self.purple = f'0;{code("purple")}'
        self.cyan = f'0;{code("cyan")}'
        self.lightgray = f'0;{code("gray")}'
        self.darkgray = f'1;{code("black")}'
        self.lightred = f'1;{code("red")}'
        self.lightgreen = f'1;{code("green")}'
        self.yellow = f'1;{code("yellow")}'
        self.lightblue = f'1;{code("blue")}'
        self.lightpurple = f'1;{code("purple")}'
        self.lightcyan = f'1;{code("cyan")}'
        #self.bold = '1'
        self.none = '0'
    def dict_codes(self):
        clr_dict = self.__dict__
        for clr in clr_dict:
            clr_dict[clr] = f'\033[{clr_dict[clr]}m'
        return clr_dict

fgcodes = Color('FG').dict_codes()
bgcodes = Color('BG').dict_codes()

class ColoredText:
    def __init__(self, text):
        self.text = text
    def parse_color(self):
        return self.parse_tokens('color')
    def raw_text(self):
        return self.parse_tokens('raw')
    def parse_tokens(self, replacer):
        parsed_text = self.text
        for key in fgcodes:
            if 'black'==key: alias = 'k'
            elif 'gray'==key: alias = 'gr'
            else: alias = key[0]
            if 'light' in key:
                if 'black' in key: alias+='k'
                elif 'gray' in key: alias+='gr'
                else:
                    alias += key[key.find('light')+len('light')]
            # print(alias)
            if replacer == 'color':
                parsed_text = parsed_text.replace(f'`f|{alias}`', fgcodes[key]).replace(f'`b|{alias}`', bgcodes[key])
            else:
                parsed_text = parsed_text.replace(f'`f|{alias}`', '').replace(f'`b|{alias}`', '')
        return parsed_text
    def __repr__(self):
        return self.parse_color()
