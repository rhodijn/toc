#!/usr/bin/env python3

def say_hi(t):
    print(t + '\n')

if __name__ == '__main__':
    say_hi('hi')

    i = 0

    while None is not True:
        i += 1
        if i > 10:
            print('\n')
            break
        print(i, end=' ')

    say_hi('bye')