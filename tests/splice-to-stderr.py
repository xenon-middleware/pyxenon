import sys

try:
    i = 1
    while True:
        line = input()
        out = "{:10} | {}".format(i, line)
        print(out, file=sys.stdout, flush=True)
        print(i, len(line.split(' ')), file=sys.stderr, flush=True)
        i += 1

except EOFError:
    pass
