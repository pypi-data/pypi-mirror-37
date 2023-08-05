from HMGeneric.terminal import TabCompleter

def get_lines_from_file(filePath='', askPhrase='What is the file Path'):
    '''Returns lines from specific file'''
    listOut = []
    if filePath == '':
        filePath = TabCompleter().completerController('path', askPhrase + ' ?\n')
    try:
        file = open(filePath, 'r')
        listOut = file.read().splitlines()
        file.close()
    finally:
        return listOut

def detect_linebreak(self, data):
        line = data.split('\n', 1)[0]
        if line.endswith('\r'):
            return '\r\n'
        else:
            return '\n'