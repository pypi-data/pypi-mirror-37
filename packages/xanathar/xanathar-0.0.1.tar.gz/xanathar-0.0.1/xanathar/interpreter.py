import lark
from xanathar import logs, strings
from xanathar import xast

class Traceback:
    file = ""
    code = ""

    def __init__(self, code="", file=""):
        self.file = file
        self.code = code

    def __str__(self):
        return "In file {0}:\n\t{1}".format(self.file, self.code)

    def __repr__(self):
        return str(self)


class Namespace:
    VARIABLES = dict()
    FUNCTIONS = dict()

    def __init__(self):
        pass


class Variable:
    value = 0
    ttype = 'Any'

    def __init__(self, t, v):
        self.ttype = t
        self.value = v


class XanatharInterpreter:
    traceback = []
    VARIABLES = dict()
    FUNCTIONS = dict()

    def __init__(self, module, builder, main, printf, xia):
        self.module = module
        self.builder = builder
        self.main = main
        self.printf = printf
        self.xia = xia

    # def evaluate(self, item):
    #    pass
        """if isinstance(item, lark.tree.Tree):
            if item.data == 'variable_setting':
                res = self.evaluate(item.children[1])
                if self.VARIABLES[item.children[0].children[0].children[0].value].ttype == 'Any' \
                         or type(res) == self.VARIABLES[item.children[0].children[0].children[0].value].ttype:
                    self.VARIABLES[item.children[0].children[0].children[0].value].value = res
            elif item.data == 'number':
                return int(item.children[0].value)
            elif item.data == 'declare_statement':
                print(item.children)
            elif item.data == 'variable_phrase':
                try:
                    print(self.VARIABLES[item.children[0].children[0].value])
                except KeyError:
                    logs.log(strings.LEVEL_ERROR, "Variable not found: %s" % item.children[0].children[0].value) # Fix with scoping

            for i in item.children:
                self.evaluate(i)"""
    def build(self, n):
        self.bt.compile(n)

    def visit(self, tree):
        self.bt = xast.BuildTree(tree, self.module, self.builder, self.main, self.printf, self.xia)
        self.bt.build()
        self.builder = self.bt.builder
        # for i in tree.children:
        #    self.evaluate(i)
