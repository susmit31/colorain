##################################################
# Error handling #
##################################################
class InvalidPropError(Exception):
    def __init__(self, msg, prop):
        self.prop = prop

    def __str__(self):
        return f'The prop {self.prop} does not exist.'

class InvalidValueError(Exception):
    def __init__(self, prop, val):
        self.prop = prop
        self.val = val
    
    def __str__(self):
        return f'The value {self.val} is invalid for prop {self.prop}.'

class UnspecifiedValueError(Exception):
    def __init__(self, prop):
        self.prop = prop
    
    def __str__(self):
        return f'The value for the prop {self.prop} is unspecified.'

class TokenSyntaxError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f'Invalid syntax for token {self.token}.'