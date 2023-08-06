from xanathar import codegen, interpreter

import os


def xcompile(parsed, name, static_int_alloc):
    cg = codegen.CodeGen()
    xp = interpreter.XanatharInterpreter(cg.module, cg.builder, cg.main, cg.printf, static_int_alloc)
    xp.visit(parsed)
    cg.create_ir(xp.builder)
    cg.save_ir(name + '.ll')

    xp.build(name)
