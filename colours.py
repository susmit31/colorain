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

def make_tokens(ground, names):
    tokens = {}
    for key in names:
        if 'black'==key: alias = 'k'
        elif 'gray'==key: alias = 'gr'
        else: alias = key[0]
        if 'light' in key:
            if 'black' in key: alias+='k'
            elif 'gray' in key: alias+='gr'
            else:
                alias += key[key.find('light')+len('light')]
        tokens[key] = f'<{"f" if ground=="FG" else "b"}={alias}>'
    return tokens

class Color:
    def __init__(self, ground):
        code = gcode(ground)
        if ground=='FG':
            self.black = f"0;{code('black')}"
            self.red = f'0;{code("red")}'
            self.green = f"0;{code('green')}"
            self.orange = f'0;{code("yellow")}'
            self.yellow = f'1;{code("yellow")}'
            self.blue = f'0;{code("blue")}'
            self.purple = f'0;{code("purple")}'
            self.cyan = f'0;{code("cyan")}'
            self.darkgray = f'1;{code("black")}'
            self.lightred = f'1;{code("red")}'
            self.lightgreen = f'1;{code("green")}'
            self.lightblue = f'1;{code("blue")}'
            self.lightpurple = f'1;{code("purple")}'
            self.lightcyan = f'1;{code("cyan")}'
        else:
            self.black = f"1;{code('black')}"
            self.red = f'1;{code("red")}'
            self.green = f"1;{code('green')}"
            self.yellow = f'1;{code("yellow")}'
            self.blue = f'1;{code("blue")}'
            self.purple = f'1;{code("purple")}'
            self.cyan = f'1;{code("cyan")}'
            self.darkgray = f'1;{code("black")}'
        self.none = '0'
    def dict_codes(self):
        clr_dict = self.__dict__
        for clr in clr_dict:
            clr_dict[clr] = f'\033[{clr_dict[clr]}m'
        return clr_dict



fgcodes = Color('FG').dict_codes()
bgcodes = Color('BG').dict_codes()
fgtokens = make_tokens('FG',fgcodes.keys())
bgtokens = make_tokens('BG', bgcodes.keys())
fgtokens['none'] = '</>'
bgtokens['none'] = '</>'

def make_code(bg = None, fg = None):
    code = ''
    if bg != None:
        code += bgcodes.get(bg) + fgcodes.get(fg)[2:]
    else:
        code += fgcodes.get(fg)
    return code