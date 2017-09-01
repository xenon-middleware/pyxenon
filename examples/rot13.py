import codecs

try:
    while True:
        line = input()
        print(codecs.encode(line, 'rot_13'))

except EOFError:
    pass
