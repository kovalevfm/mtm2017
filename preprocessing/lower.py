#! /usr/bin/env python
import sys

def main():
    for l in sys.stdin:
        l = l.strip('\n').decode('utf-8').lower()
        print l.encode('utf-8')

if __name__ == "__main__":
    main()
