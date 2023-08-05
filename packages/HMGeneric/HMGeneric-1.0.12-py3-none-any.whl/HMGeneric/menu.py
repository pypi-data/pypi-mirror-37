import sys

class MenuRoot:
            
    def __init__(self, globalVars):
        self.banner = None
        self.branches = []
        self.currentBranch: self.MenuBranch = None
        self.globalVars = globalVars
    
    def add_branch(self, name, title = None):
        menuBranch = self.MenuBranch(self, name=name, title=title)
        self.branches.append(menuBranch)

    def set_current_branch(self, name):
        for branch in self.branches:
            if(branch.name == name):
                self.currentBranch = branch
                self.currentBranch.show()
                return
        print("There is no menu with the name '"+name+"'")

    def get_branch(self, name):
        for branch in self.branches:
            branch: self.MenuBranch
            if(branch.name == name):
                return branch
        return None

    class MenuBranch:

        def __init__(self, menuRoot, name, title = None, parentBranch = None):
            self.name = name
            self.title = title
            self.options = []
            self.parentBranch = parentBranch
            self.menuRoot = menuRoot

        def show(self):
            while True:
                if(self.title):
                    print(self.title)
                for counter, option in enumerate(self.options, 1):
                    print(str(counter) + ". " + option.phrase)
                if(self.parentBranch):
                    print('0. Back')
                else:
                    print('0. Exit')

                chose = input('Enter the option number:\n')
                if(chose.isdigit()):
                    chose = int(chose)
                    if(chose == 0):
                        if(self.parentBranch):
                            self.menuRoot.set_current_branch(self.parentBranch)
                        else:
                            sys.exit(0)
                    if((chose-1) in range(0,len(self.options))):
                        self.options[chose-1].run()

        def add_menu_option(self, targetBranch, defenition, phrase, passRoot = False):
            menuOption = self.MenuOption()
            menuOption.menuRoot = self.menuRoot
            menuOption.targetBranch = targetBranch
            menuOption.defenition = defenition
            menuOption.phrase = phrase
            menuOption.passRoot = passRoot
            self.options.append(menuOption)

        class MenuOption:

            def __init__(self):
                self.menuRoot : MenuRoot
                self.targetBranch : str
                self.defenition : callable
                self.phrase : str
                self.passRoot : bool
            
            def run(self):
                if(self.passRoot):
                    self.defenition(self.menuRoot)
                else:
                    self.defenition()
                self.menuRoot.set_current_branch(name=self.targetBranch)

def select_from_list(List: list, phrase):
        print(phrase)
        for counter, obj in enumerate(List, 1):
            print(str(counter) + ". " + obj)
        while True:
            chose = input('Enter the option number:\n')
            if(chose.isdigit()):
                chose = int(chose)-1
                if(chose in range(0, len(List))):
                    return List[chose]