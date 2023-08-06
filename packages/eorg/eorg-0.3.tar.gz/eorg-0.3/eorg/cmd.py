import os
import sys
from eorg.parser import parse
from eorg.generate import html



def tangle(doc):
    print("tangle")
    code = getattr(doc, 'code')
    print(code)

def recursive(path):
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".org"):
                yield root + os.sep + filename

def tokenize(doc):
    for item in doc:
        print(item)

def htmlize(doc):
    for item in doc:
        print(item)

def handler(fp, kwargs):
    if kwargs.s is True:
        tokenize(doc)
    if kwargs.t is True:
        tangle(doc)
    if kwargs.w is True:
        print(html(doc).read())
    if kwargs.meta:
        values = {}
        for item in kwargs.meta:
            values[item] = getattr(doc, item)
        print(' | '.join([k + ' - ' + v for k,v in values.items()]))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process some .org files")
    parser.add_argument("filename")
    parser.add_argument('-r', action='store_true', help='recursive')
    parser.add_argument('-w', action='store_true', help='Generate html')
    parser.add_argument('-s', action='store_true', help='Document structure')
    parser.add_argument('-t', action='store_true', help='Tangle out code')
    parser.add_argument('-m', '--meta', action='append', help='Show meta data')
    parser.add_argument(
        "--tangle",
        dest="tangle",
        const=tangle,
        default=False,
        action="store_const",
        help="Tangle the source code",
    )

    args = parser.parse_args()
    filename = os.path.abspath(args.filename)


    if args.r is True:
        for filename in recursive(filename):
            with open(filename, "r") as fp:
                doc = parse(fp)
                handler(parse(fp), args)
        sys.exit()

    with open(filename, "r") as fp:
        doc = parse(fp)
        handler(parse(fp), args)


