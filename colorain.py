from colours import *

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