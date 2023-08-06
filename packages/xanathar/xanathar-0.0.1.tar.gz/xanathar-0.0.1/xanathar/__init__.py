# LICENSE
# inspiration: https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
__DEBUG__ = False

import lark
import argparse
from xanathar import compiler
from xanathar import logs
from xanathar import strings
import os, sys

if __DEBUG__:
    sys.stdout = open('stdout', 'w')

cdir = os.path.dirname(__file__)
GRAMMAR_FILE = cdir + "/grammar/GRAMMAR.ebnf"
with open(GRAMMAR_FILE) as file:
    lark_parser = lark.Lark(file.read())


def main():
    parser = argparse.ArgumentParser(description='Runs Xanathar.')
    parser.add_argument('-a', dest='ast', action='store_const',
                        const=True, default=False,
                        help='print the ast after parsing')
    parser.add_argument("file")
    parser.add_argument('-o', nargs='?', help='out file for the generated LLVM')
    parser.add_argument('--static-int-alloc', dest='ia', nargs="?", default=32,
                        help="static allocation size (bits) for integers")

    args = parser.parse_args()

    try:
        with open(args.file) as in_file:
            parsed = lark_parser.parse(in_file.read())
            if args.o:
                name = args.o
            else:
                name = in_file.name
            if args.ast:
                print(parsed.pretty())
        compiler.xcompile(parsed, name, int(args.ia))

    except lark.exceptions.ParseError as e:
        logs.log(strings.LEVEL_ERROR, strings.PARSE_ERR)


if __name__ == "__main__":
    main()
# TODO: implement soon: pointers
# TODO: implement later (arrays, strings, io, file io, argc/argv, )
