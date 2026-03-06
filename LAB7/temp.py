import sys
paths = sys.path
num = 1
for path in paths:
    print('{}. {}'.format(num, path))
    num += 1