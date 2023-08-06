import sys


def log(lvl, msg):
    sys.stderr.write(lvl + " " + msg + "\n")
