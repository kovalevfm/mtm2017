# coding: utf-8
import sys
import math
import argparse

from vowpalwabbit import pyvw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='vw model')
    args = parser.parse_args()

    p = pyvw.vw(i=args.model, t=True, quiet=True)
    for cnt, l in enumerate(sys.stdin):
        src = l.strip('\n')
        src = src.replace("|", "PIPE").replace(":", "COLON")
        print 1/(1+math.exp(-p.predict(" | {0}".format(src))))

if __name__ == '__main__':
    main()
