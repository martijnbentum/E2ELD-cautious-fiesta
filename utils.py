import string

def remove_numeric(s):
    output = ''
    for char in s:
        if char in string.digits:continue
        output += char
    return output

def get_number(s):
    for char in s:
        if char in string.digits: return int(char)
    return 0

