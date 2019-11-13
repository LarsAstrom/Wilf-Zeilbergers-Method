import sys

def read_content(file = None):
    lines = get_lines(file)
    return lines

def get_lines(file):
    if file == None:
        return sys.stdin.read().strip().split('\n')
    else:
        return open(file,'r').read().strip().split('\n')

def test(file = None):
    for line in read_content(file):
        
