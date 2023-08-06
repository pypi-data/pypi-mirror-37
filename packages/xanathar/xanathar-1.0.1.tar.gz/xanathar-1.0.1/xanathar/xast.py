from llvmlite import ir
from llvmlite import binding
import lark
import lark.tree
import json
import os

PREDEFINED_FUNCTIONS = {}
NAMESPACES = {}
VARIABLES = {}
MODULES = {
    'stdio': 'stdlib/stdio.xl',
    'stdlib': 'stdlib/stdlib.xl'
}


class IntDummy:
    pass


class FloatDummy:
    pass


class UIntDummy(IntDummy):
    pass


class Namespace:
    name = ""
    vars_ = {}
    fns = {}

    def __init__(self, name):
        self.name = name

    def add_var(self, var, res):
        self.vars_[var] = res

    def get_var(self, var):
        return self.vars_[var]

    def add_fn(self, fn, res):
        self.fns[fn] = res

    def get_fn(self, fn):
        return self.fns[fn]


class BasicAst:
    def __init__(self, builder: ir.IRBuilder, module: ir.Module):
        self.builder = builder
        self.module = module

    def eval(self): pass


class BasicAstValue(BasicAst):
    def __init__(self, builder, module, value):
        super().__init__(builder, module)
        self.value = value


class Float(BasicAstValue, FloatDummy):
    def eval(self):
        i = ir.Constant(ir.FloatType(), float(self.value))
        return i


class String(BasicAstValue):
    def __init__(self, builder, module, value):
        value = value.encode('utf-8').decode('unicode_escape')
        super().__init__(builder, module, value)

        self.mem_addr = self.builder.alloca(ir.ArrayType(ir.IntType(8), len(self.value)))
        self.builder.store(ir.Constant(ir.ArrayType(ir.IntType(8), len(self.value)),
                                       [ord(x) for x in self.value]), self.mem_addr)
        self.i32_const = ir.Constant(ir.IntType(32), 0)
        self.lead_ptr = self.builder.gep(self.mem_addr, [self.i32_const])
        # print(self.lead_ptr)

        # self.ptrs = []
        # chrs = [ord(x) for x in self.value]
        # for i in chrs:
        #     cptr = builder.alloca(ir.IntType(8))
        #     self.ptrs.append(cptr)
        #     value = ir.Constant(ir.IntType(8), i)
        #     builder.store(value, cptr)

        # self.v = ir.Constant(ir.ArrayType(ir.IntType(8), len(self.value)), [ord(x) for x in self.value])

    def eval(self):
        # i = ir.Constant(ir.ArrayType(ir.IntType(8), len(self.value)), [ord(x) for x in self.value])
        # voidptr_ty = ir.IntType(8).as_pointer()
        # value_ = ir.Constant(ir.IntType(32), 0)
        # value = self.builder.extract_value(self.v, 0)
        # value = self.builder.gep(self.v, [value_, value_])
        # print(value.type)
        return self.lead_ptr
        # self.builder.bitcast(value, voidptr_ty)

    def __eq__(self, other):
        return self.value == other.value


TYPES = {
    'float': ir.FloatType(),
    'void': ir.VoidType(),
}

for __bits in [1, 8, 16, 32, 64, 128, 256, 512, 1024]:
    globals()["Int" + str(__bits)] = type("Int" + str(__bits), (BasicAstValue,IntDummy),
                                          {'eval': lambda self: ir.Constant(ir.IntType(__bits), int(self.value))})
    globals()["UInt" + str(__bits)] = type("UInt" + str(__bits), (BasicAstValue,UIntDummy),
                                           {'eval': lambda self: ir.Constant(ir.IntType(__bits), abs(int(self.value)))})

    TYPES["int%d" % __bits] = ir.IntType(__bits)
    TYPES["uint%d" % __bits] = ir.IntType(__bits)

    # such dynamic, much usefulness


class BinaryOp(BasicAst):
    def __init__(self, builder, module, left, right):
        super().__init__(builder, module)
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.add(l, r)
        elif isinstance(l, FloatDummy) and isinstance(r, FloatDummy):
            return self.builder.fadd(l, r)


class Sub(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.sub(l, r)
        elif isinstance(l, FloatDummy) and isinstance(r, FloatDummy):
            return self.builder.fsub(l, r)


class Mul(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.mul(l, r)
        elif isinstance(l, FloatDummy) and isinstance(r, FloatDummy):
            return self.builder.fmul(l, r)


class Div(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, UIntDummy) and isinstance(r, UIntDummy):
            return self.builder.udiv(l, r)
        elif isinstance(l, FloatDummy) and isinstance(r, FloatDummy):
            return self.builder.fdiv(l, r)
        elif isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.sdiv(l, r)


class Mod(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, UIntDummy) and isinstance(r, UIntDummy):
            return self.builder.urem(l, r)
        elif isinstance(l, FloatDummy) and isinstance(r, FloatDummy):
            return self.builder.frem(l, r)
        elif isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.srem(l, r)


class And(BinaryOp):
    def eval(self):
        l = self.left
        r = self.right
        if isinstance(l, IntDummy) and isinstance(r, IntDummy):
            return self.builder.and_(l, r)


class Rol(BasicAst):
    pass


class Ror(BasicAst):
    def __init__(self, build, mod, a1, a2):
        super().__init__(build, mod)
        self.a1 = a1
        self.a2 = a2

    def eval(self):
        if self.a1.type.__class__ not in [ir.IntType, ir.FloatType]:
            gep = self.builder.gep(self.a1, [self.a2])
            return self.builder.bitcast(gep, ir.PointerType(ir.IntType(8)))
        return self.builder.ashr(self.a1, self.a2)


class Bor(BasicAst):
    pass


class Xor(BasicAst):
    pass


class Not(BasicAst):
    pass


class Rng(BasicAst):
    pass


class Ceq(BasicAst):
    def __init__(self, build, mod, a1, a2):
        super().__init__(build, mod)
        self.a1 = a1
        self.a2 = a2

    def eval(self):
        if self.a1.type.__class__ == ir.IntType:
            return self.builder.icmp_signed("==", self.a1, self.a2)
        elif self.a1.type.__class__ == ir.FloatType:
            return self.builder.fcmp_ordered("==", self.a1, self.a2)
        else:
            return ir.Constant(ir.IntType(1), self.a1 == self.a2)


class Ois(BasicAst):
    pass


class cast(BasicAst):
    pass


class use_statement(BasicAst):
    pass


class declare_statement(BasicAst):
    def __init__(self, builder, module, variable, type_):
        super().__init__(builder, module)
        self.var = variable
        self.type = type_

    def eval(self):
        super().eval()
        ptr = self.builder.alloca(self.type)
        VARIABLES[self.var] = ptr


class variable_phrase(BasicAst):
    def __init__(self, builder, module, var):
        super().__init__(builder, module)
        self.var = var

    def eval(self):
        super().eval()
        return self.builder.load(VARIABLES[self.var])


class as_phrase(BasicAst):
    pass


class variable_setting(BasicAst):
    def __init__(self, builder, module, var, val):
        super().__init__(builder, module)
        self.var = var
        self.val = val

    def eval(self):
        self.builder.store(self.val, VARIABLES[self.var])


class fncall(BasicAst):
    def __init__(self, builder, module, fn, vars):
        super().__init__(builder, module)
        self.fn = fn
        self.vars = vars

    def eval(self):
        super().eval()
        return self.builder.call(self.fn, self.vars)


class ptr(BasicAst):
    def __init__(self, builder, module, var):
        super().__init__(builder, module)
        self.var = var

    def eval(self):
        c = ir.Constant(self.var.type.as_pointer(), self.var)
        return c


class Deref(BasicAst):
    def __init__(self, builder, module, var: ir.Constant):
        super().__init__(builder, module)
        self.var = var

    def eval(self):
        c = ir.Constant(self.var.type.pointee, self.var)
        return c


class fn(BasicAst):
    pass


class if_(BasicAst):
    pass


class for_(BasicAst):
    pass


class while_(BasicAst):
    pass


class ret(BasicAst):
    pass


class varspec(BasicAst):
    pass


def printf_(value, builder, module, printf):
    voidptr_ty = ir.IntType(8).as_pointer()
    fmt = "%i \n\0"
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                        bytearray(fmt.encode("utf8")))

    global_fmt = ir.GlobalVariable(module, c_fmt.type, name="fstr")
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    fmt_arg = builder.bitcast(global_fmt, voidptr_ty)

    builder.call(printf, [fmt_arg, value], "printf")


class BuildTree(BasicAst):
    phrases = []

    def __init__(self, lark_tree: lark.tree.Tree, module, builder: ir.IRBuilder, main: ir.Function, printf, static_int_alloc, noinit=False):
        self.printf = printf
        super().__init__(builder, module)
        if not noinit:
            self.setup()

        for i in lark_tree.children:
            self.phrases.append(i.children[0])

        self.ia = static_int_alloc

        self.ret = ir.VoidType()
        self.old_builder = ir.IRBuilder()
        # self.engine = engine

        self.is_void = True

        self.main = main

        self.cmpops = {
            'leq': '<=',
            'geq': '>=',
            'les': '<',
            'gre': '>',
        }

        self.LOADED_MODULES = []

        # builder.call(printf, [fmt_arg, String(builder, module, "abcd").eval()], "printf")
        # printf_(ir.Constant(ir.IntType(8), 41), builder, module, printf)

        # PARSE lark_tree #

    def __setup_default_namespaces(self):
        global NAMESPACES

        std = Namespace("std")
        std.add_fn("print", self.printf)
        NAMESPACES["std"] = std

    def __setup_default_functions(self):
        global PREDEFINED_FUNCTIONS

        PREDEFINED_FUNCTIONS["print_i"] = self.printf
        PREDEFINED_FUNCTIONS["print_x"] = self.printf
        PREDEFINED_FUNCTIONS["print_s"] = self.printf
        PREDEFINED_FUNCTIONS["print_c"] = self.printf
        PREDEFINED_FUNCTIONS["printf"] = self.printf

        #FILE = self.module.context.get_identified_type("FILE")
        #i8_ptr = ir.IntType(8).as_pointer()
        #i32 = ir.IntType(32)
        #fgets_ty = ir.FunctionType(i8_ptr, [i8_ptr, i32, FILE.as_pointer()])
        #fgets = ir.Function(self.module, fgets_ty, name="fgets")
        #PREDEFINED_FUNCTIONS["fgets"] = fgets

        #fdopen_ty = ir.FunctionType(FILE.as_pointer(), [i32, i8_ptr])
        #fdopen = ir.Function(self.module, fdopen_ty, name="fdopen")
        #PREDEFINED_FUNCTIONS["fdopen"] = fdopen

    def __setup_default_variables(self):
        # FILE = self.module.context.get_identified_type("FILE")
        fmt_val = ir.Constant(ir.ArrayType(ir.IntType(8), 2), bytearray("r\00".encode('utf-8')))
        fmt = ir.GlobalVariable(self.module, fmt_val.type, "fdopen_fmt")
        fmt.linkage = 'internal'
        fmt.global_constant = True
        fmt.initializer = fmt_val

        #local_fmt = self.builder.bitcast(fmt, ir.IntType(8).as_pointer())
        #stdin = self.builder.call(PREDEFINED_FUNCTIONS["fdopen"], [ir.IntType(32)(0), local_fmt]) # self.builder.alloca(FILE)
        # self.builder.store(self.builder.call(PREDEFINED_FUNCTIONS["fdopen"], [ir.IntType(32)(0), local_fmt]), stdin)
        #VARIABLES["stdin"] = stdin

    def __init_hook(self):
        self.voidptr_ty = ir.IntType(8).as_pointer()

        self.global_fmts = {}

        for fmt_str in "ixsc":
            fmt = "%s%%%s \n\0" % ("0x" if fmt_str == 'x' else '', fmt_str)
            c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))

            global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="%sstr" % fmt_str)
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = c_fmt

            self.global_fmts[fmt_str] = self.builder.bitcast(global_fmt, self.voidptr_ty)

    def setup(self):
        self.__setup_default_namespaces()
        self.__setup_default_functions()
        self.__setup_default_variables()
        self.__init_hook()

    def _parse_comp_op(self, op, i):
        v1 = self.parse_phrase(i.children[0])
        v2 = self.parse_phrase(i.children[1])

        if v1.type.__class__ == ir.IntType:
            return self.builder.icmp_signed(op, v1, v2)
        elif v1.type.__class__ == ir.FloatType:
            return self.builder.fcmp_ordered(op, v1, v2)

    def to_type(self, i: str):
        if '*' in i:
            base = TYPES[i.replace('*', '')]
            for i in range(i.count('*')):
                base = ir.PointerType(base)
            return base
        else:
            return TYPES[i]

    def compile(self, name):
        command = 'clang ' + name + '.ll '
        for i in self.LOADED_MODULES:
            if i["type"] == 'LINKED_SO':
                command += os.path.abspath(i["FILE"]) + ' '
        os.system(command + '-o ' + name + '.o')

    def add_module(self, mod):
        mod = MODULES[mod]
        with open(os.path.abspath(mod)) as mf:
            mod_txt = mf.read()
        module = json.loads(mod_txt)
        if module["type"] == "LINKED_SO":
            binding.load_library_permanently(module["FILE"])

        for k in module["FUNCTIONS"]:
            ftype = ir.FunctionType(self.to_type(module["FUNCTIONS"][k][0]),
                                    [self.to_type(q) for q in module["FUNCTIONS"][k][1]])
            fxn = ir.Function(self.module, ftype, k)
            PREDEFINED_FUNCTIONS[k] = fxn

        self.LOADED_MODULES.append(module)

    def parse_phrase(self, i):
        global VARIABLES

        if i.data == 'declare_statement':
            try:
                declare_statement(self.builder, self.module, i.children[0].children[0].children[0].value,
                                  TYPES[i.children[1].children[0].children[0].children[0].value]).eval()
            except AttributeError:
                base_type = TYPES[i.children[1].children[0].children[1].children[0].children[0].value]
                for t in i.children[1].children[0].children[0].value:
                    if t == '*':
                        base_type = ir.PointerType(base_type)
                declare_statement(self.builder, self.module, i.children[0].children[0].children[0].value,
                                  base_type).eval()
        elif i.data == 'fncall':
            fnname = i.children[0].children[0]
            if 'print' in fnname and fnname[-1] in self.global_fmts:
                args = [self.global_fmts[fnname.value[-1]]] + [self.parse_phrase(x.children[0]) for x in i.children[1:]]
            else:
                args = [self.parse_phrase(x.children[0]) for x in i.children[1:]]
            fn = PREDEFINED_FUNCTIONS[i.children[0].children[0].value]
            return fncall(self.builder, self.module, fn, args).eval()
        elif i.data == 'variable_phrase':
            return variable_phrase(self.builder, self.module, i.children[0].children[0].value).eval()
        elif i.data == 'variable_setting':
            return variable_setting(self.builder, self.module, i.children[0].children[0].children[0].value,
                                    self.parse_phrase(i.children[1])).eval()
        elif i.data == 'ptr':
            return ptr(self.builder, self.module, self.parse_phrase(i.children[0])).eval()
        elif i.data == 'deref':
            return Deref(self.builder, self.module, self.parse_phrase(i.children[0])).eval()
        elif i.data == 'expression':
            return self.parse_phrase(i.children[0])
        elif i.data == 'number':
            return ir.Constant(ir.IntType(self.ia), int(i.children[0]))
        elif i.data == 'float':
            return ir.Constant(ir.FloatType(), float(i.children[0]))
        elif i.data == 'cast':
            val_to_cast = self.parse_phrase(i.children[0])
            t1 = val_to_cast.type
            t2 = TYPES[i.children[1].children[0].children[0].children[0].value]
            if t1.__class__ == ir.IntType and t2.__class__ == ir.FloatType:
                return self.builder.sitofp(val_to_cast)
            elif t1.__class__ == ir.FloatType and t2.__class__ == ir.IntType:
                return self.builder.fptosi(val_to_cast)
            elif t1.__class__ == ir.IntType and t2.__class__ == ir.IntType:
                if t1.width > t2.width:
                    return self.builder.trunc(val_to_cast, t2)
                elif t1.width < t2.width:
                    return self.builder.zext(val_to_cast, t2)
                else:
                    return val_to_cast
            elif t1.__class__ == ir.FloatType and t2.__class__ == ir.FloatType:
                return val_to_cast
            else:
                return self.builder.bitcast(val_to_cast, t2)
        elif i.data == 'str':
            return String(self.builder, self.module, i.children[0].value[1:-1] + '\00').eval()
        elif i.data == 'ror':
            return Ror(self.builder, self.module, self.parse_phrase(i.children[0]),
                       self.parse_phrase(i.children[1])).eval()
        elif i.data == 'ceq':
            return Ceq(self.builder, self.module, self.parse_phrase(i.children[0]),
                       self.parse_phrase(i.children[1])).eval()
        elif i.data == 'mod':
            return self.builder.srem(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'fn':
            # get type
            ret_str = i.children[2].children[0].children[0].children[0].value
            ret = TYPES[ret_str]
            self.ret = ret
            self.is_void = (ret_str == 'void')
            args = []
            vars_ = []
            for j in i.children[1].children:
                if j.data == 'as_phrase':
                    args.append(TYPES[j.children[0].children[0].children[0].value])
                else:
                    vars_.append(j.children[0].children[0].value)
            ftype = ir.FunctionType(ret, args)
            name = i.children[0].children[0].value
            f = ir.Function(self.module, ftype, name)
            PREDEFINED_FUNCTIONS[name] = f
            block = f.append_basic_block("entry")
            b = ir.IRBuilder(block)

            for q in range(len(f.args)):
                ptrl = b.alloca(f.args[q].type)
                b.store(f.args[q], ptrl)
                VARIABLES[vars_[q]] = ptrl

            self.old_builder = self.builder
            old_VARIABLES = VARIABLES
            self.builder = b

            for q in i.children[3:]:
                self.parse_phrase(q.children[0])

            self.builder = self.old_builder
            VARIABLES = old_VARIABLES
        elif i.data == 'if':
            with self.builder.if_else(self.parse_phrase(i.children[0])) as (ifs, other):
                if_statements = i.children[1:-1]
                else_statements = []
                if i.children[-1].data == 'else':
                    else_statements = i.children[-1].children
                else:
                    if_statements.append(i.children[-1])
                with ifs:
                    for stmt in if_statements:
                        self.parse_phrase(stmt.children[0])
                with other:
                    for stmt in else_statements:
                        self.parse_phrase(stmt.children[0])
        elif i.data == 'ret':
            if self.is_void:
                self.builder.ret_void()
            else:
                val = self.parse_phrase(i.children[0])
                self.builder.ret(val)
        elif i.data == 'add':
            return self.builder.add(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'sub':
            return self.builder.sub(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'mul':
            return self.builder.mul(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'div':
            return self.builder.sdiv(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1])) # TODO: for div and mod, include s/u/f
        elif i.data == 'for':
            p1 = i.children[0].children[0]
            e = i.children[1].children[0]
            p2 = i.children[2].children[0]

            try:
                phrases = i.children[3:]
            except IndexError:
                return

            id_ = 0
            for q in self.builder.function.basic_blocks:
                if q.name == 'forloop-' + str(id_):
                    id_ += 1

            curr_for = self.builder.append_basic_block("forloop-" + str(id_))
            end_for = self.builder.append_basic_block("endfor-" + str(id_))

            self.parse_phrase(p1)
            self.builder.branch(curr_for)
            self.builder = ir.IRBuilder(curr_for)

            for q in phrases:
                self.parse_phrase(q.children[0])

            self.parse_phrase(p2)
            self.builder.cbranch(self.parse_phrase(e), curr_for, end_for)

            self.builder = ir.IRBuilder(end_for)

        elif i.data == 'while':
            value = i.children[0]

            try:
                phrases = i.children[1:]
            except IndexError:
                return

            id_ = 0
            for q in self.builder.function.basic_blocks:
                if q.name == 'whileloop-' + str(id_):
                    id_ += 1

            curr_while = self.builder.function.append_basic_block("entry.whileloop" + str(id_))
            end_while = self.builder.function.append_basic_block("entry.endwhile" + str(id_))
            self.builder.branch(curr_while)
            self.builder = ir.IRBuilder(curr_while)

            for q in phrases:
                self.parse_phrase(q.children[0])

            self.builder.cbranch(self.parse_phrase(value), curr_while, end_while)

            self.builder = ir.IRBuilder(end_while)
        elif i.data == 'les' or i.data == 'gre' or i.data == 'leq' or i.data == 'geq':
            return self._parse_comp_op(self.cmpops[i.data], i)
        elif i.data == 'rol':
            return self.builder.lshr(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'bor':
            return self.builder.or_(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'xor':
            return self.builder.xor(self.parse_phrase(i.children[0]), self.parse_phrase(i.children[1]))
        elif i.data == 'not':
            return self.builder.not_(self.parse_phrase(i.children[0]))
        elif i.data == 'use_statement':
            self.add_module(i.children[0].children[0].value)
        elif i.data == 'raw_var':
            return VARIABLES[i.children[0].children[0].value]

    def build(self):
        for i in self.phrases:
            self.parse_phrase(i)


class PhraseList(BasicAst):
    def __init__(self, module, builder: ir.IRBuilder):
        super().__init__(builder, module)

# TODO implement later: modules (use), arrays (rng)
