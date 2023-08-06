from llvmlite import ir, binding

HEADER = """%FILE = type opaque
declare %FILE* @fdopen(i32, i8*)
@r = constant [2 x i8] c"r\\00"
declare i8* @"fgets"(i8*, i32, %FILE*)

"""

MAIN_HEADER = """
  %".1" = bitcast [2 x i8]* @r to i8*
  %stdin = call %FILE* @fdopen(i32 0, i8* %".1")
  
"""

# TODO: add header somehow

# borrowed from https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
# :)


class CodeGen:
    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()
        self._config_llvm()
        self._create_execution_engine()
        self._declare_print_function()

    def _config_llvm(self):
        # Config LLVM
        self.module = ir.Module(name=__file__)
        self.module.triple = self.binding.get_process_triple()
        func_type = ir.FunctionType(ir.VoidType(), [], False)
        base_func = ir.Function(self.module, func_type, name="main")
        self.main = base_func
        block = base_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

    def _create_execution_engine(self):
        """
        Create an ExecutionEngine suitable for JIT code generation on
        the host CPU.  The engine is reusable for an arbitrary number of
        modules.
        """
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        # And an execution engine with an empty backing module
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

    def _declare_print_function(self):
        # Declare Printf function
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

    def _compile_ir(self, builder):
        """
        Compile the LLVM IR string with the given engine.
        The compiled module object is returned.
        """
        # Create a LLVM module object from the IR
        self.builder = builder
        self.builder.ret_void()
        self.module.add_named_metadata("gen-by", ["Xanathar"])
        llvm_ir = str(self.module)
        mod = self.binding.parse_assembly(llvm_ir)

        mod.verify()
        # Now add the module and make sure it is ready for execution
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod

    def create_ir(self, b):
        self._compile_ir(b)

    def save_ir(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(str(self.module))
