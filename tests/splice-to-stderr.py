import sys

try:
    i = 1
    while True:
        line = input()
        out = "{:10} | {}".format(i, line)
        if len(line) % 2 == 0:
            print(out, file=sys.stdout)
        else:
            print(out, file=sys.stderr)
        i += 1

except EOFError:
    pass
