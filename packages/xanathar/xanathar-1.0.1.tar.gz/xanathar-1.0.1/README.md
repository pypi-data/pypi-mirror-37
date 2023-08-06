# Xanathar
###### Name inspired by *Xanathar's Guide to Everything* (© Wizards of the Coast)

## Pipeline
###### Made in draw.io

![Xanathar Pipeline](http://cdn.supachat.net/Xanathar_Pipeline.png)

## Features
+ Compiles directly to a binary (through LLVM IR)
+ Fast (uses [Lark](https://github.com/lark-parser/lark) and [LLVMLite](https://github.com/numba/llvmlite)) for speed
+ Strong typing (enforced by LLVM IR)
+ Easy to learn syntax
+ Written in Python, so no installation required
## Spec

### Implemented operations 
###### Keep in mind, Xanathar is a *huge* WIP

+ Variables (statically allocated)
    + Int / UInt
        + 1 Bit (Bool)
        + 8 Bit (Char)
        + 16 Bit
        + 32 Bit
        + 64 Bit
        + 128 Bit
        + 512 Bit
        + 1024 Bit
    + Floats
    + Strings (implemented as a statically allocated int8[])
+ Printing
    + libc `printf` can be used
    + `print_s`, `print_i`, `print_x`, `print_c` print with the `printf` format string (`%s` for `print_s`, etc.)
        + Implemented as a libc call to `printf` with the corresponding format string
        + Deprecated in favour of `printf`
+ Casting
    + Works!
    + `string >> int` gives pointer to the `int`'th character in `string`
        + useful for (e.g.) `printf`
+ Loops
    + While and For
        + While loops: more like a C-style do-while
        + For loops: similar to a do-while style loop
+ Modules
    + stdio
        + `i8* get[i8*, i32]`
            + Implements `fgets` in C (source can be viewed in `stdlib/stdio.c`)
        

It's the best of both worlds: it keeps the amazing speed of low-level languages, but with the power and ease of high-level languages.
On a test of the Collatz conjecture, run for i = 1 to 10, and 77,031, (100 runs of the entire program) Python 3 ran in 1.9s, whereas Xanathar ran in 0.064s. 
For 1000 runs of the program, Python 3 took 20.7s whereas Xanathar took 0.531s.