import subprocess, os, sys, glob

if(os.name == 'nt'):
    from pyreadline import Readline
else:
    from readline import Readline


from HMGeneric.array import count_layers
from HMGeneric.parse import get_object_unbyte

def get_terminal_lines(CMD, startLine=0):
    '''Run terminal command and get its output'''
    if(count_layers(CMD)>1):
        procs = []
        for i in range(0,len(CMD)):
            if(i==0):
                proc = subprocess.Popen(CMD[i], stdout=subprocess.PIPE)
                procs.append(proc)
            else:
                proc = subprocess.Popen(CMD[i], stdin=procs[i-1].stdout,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                procs.append(proc)

        for i in range(0,len(procs)-1):
            procs[i].stdout.close()

        out, err = procs[-1].communicate()
        return(bytes(out).decode())
    else:
        CMDOutLines = []
        with subprocess.Popen(CMD, stdout=subprocess.PIPE, bufsize=1,
                            universal_newlines=True) as p:
            for line in p.stdout:
                CMDOutLines.append((get_object_unbyte(line)))
        return CMDOutLines[startLine:len(CMDOutLines)]

def check_admin_rights(exitIfNot = False):
    import ctypes
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if(exitIfNot == True):
        if(is_admin == False):
            print("Please start this code with admin rights")
            sys.exit(0)
    return is_admin

class TabCompleter:
    """
    A tab completer that can either complete from
    the filesystem or from a list.
    Partially taken from:
    http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw
    """
    def __init__(self):
        self.readline = Readline()
    def completerController(self, ListOrPath, QPhrase):
        """
        This is the tab completer controller.
        """
        self.readline.set_completer_delims('\t')
        self.readline.parse_and_bind('tab: complete')
        if(ListOrPath == 'list'):
            self.readline.set_completer(self.listCompleter)
        else:
            self.readline.set_completer(self.pathCompleter)
        return input(QPhrase)

    def pathCompleter(self, text, state):
        """
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line = self.readline.get_line_buffer().split()

        if '~' in text:
            text = os.path.expanduser('~')

        if os.path.isdir(text):
            text += '/'

        return [x for x in glob.glob(text + '*')][state]

    def createListCompleter(self, listValues):
        """
        This is a closure that creates a method that autocompletes from
        the given list.
        Since the autocomplete function can't be given a list to complete from
        a closure is used to create the listCompleter function with a list
        to complete
        from.
        """

        def listCompleter(text, state):
            line = self.readline.get_line_buffer()

            if not line:
                return [c + " " for c in listValues][state]

            else:
                return [c + " " for c in listValues if c.startswith(line)][state]

        self.listCompleter = listCompleter