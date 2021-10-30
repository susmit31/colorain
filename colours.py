# Styling codes
CLR_CODE = {
    'black':0,
    'red':1,
    'green':2,
    'yellow':3,
    'blue':4,
    'purple':5,
    'cyan':6,
}

FMT_CODE = {
    'B':1, # bold
    'I': 3, # italic
    'U':4 # underline
}

# Foreground and background
GRD_CODE = {'BG':4, 'FG':3}

# Returns a function that returns the code for using a colour in
# the foreground or the background
def gcode(ground):
    return lambda clr: f"{GRD_CODE[ground]}{CLR_CODE[clr]}"

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
        tokens[key] = f'{"f" if ground=="FG" else "b"}={alias}'
    return tokens

def parse_token(token):
    parsed_token = {}
    fmt_tags = ['B', 'I', 'U']
    for subtoken in token:
        if len(subtoken):
            if subtoken[0]=='f':
                parsed_token['fg'] = fg_abbrs[subtoken.split('=')[1].strip()]
            elif subtoken[0]=='b':
                parsed_token['bg'] = bg_abbrs[subtoken.split('=')[1].strip()]
            elif subtoken[0] in fmt_tags:
                tag = fmt_tags[fmt_tags.index(subtoken[0])]
                parsed_token[tag] = True
            elif subtoken[0]=='/':
                parsed_token['end'] = True
    return token_to_code(**parsed_token)

def token_to_code(bg = None, fg = None, B=None, I=None, U=None, end=None):
    code = '\033['
    if bg: code += f"{bgcodes[bg]};"
    if fg: code += f"{fgcodes[fg]};"
    if B: code += f"{FMT_CODE['B']};"
    if U: code += f"{FMT_CODE['U']};"
    if I: code += f"{FMT_CODE['I']};"
    if end: code += f"{fgcodes['end']};"
    code = code.strip(';')
    code += "m"
    return code

def make_clrcodes():
    fgcodes = {}
    bgcodes = {}
    
    make_fgcode = gcode('FG')
    make_bgcode = gcode('BG')
    
    for clr in CLR_CODE:
        fgcodes['orange' if clr=='yellow' else clr] = make_fgcode(clr)
        bgcodes[clr] = make_bgcode(clr)
    for clr in CLR_CODE:
        fgcodes[clr if clr=='yellow' else ('gray' if clr=='black' else 'light'+clr)] = f'1;{make_fgcode(clr)}' 

    return fgcodes, bgcodes

fgcodes, bgcodes = make_clrcodes()
fgcodes['end'], bgcodes['end'] = '0','0'

fgtokens = make_tokens('FG',fgcodes.keys())
bgtokens = make_tokens('BG', bgcodes.keys())

fg_abbrs = {fgtokens[k].split('=')[1]:k for k in fgtokens}
bg_abbrs = {bgtokens[k].split('=')[1]:k for k in bgtokens}

fgtokens['end'] = '</>'
bgtokens['end'] = '</>'