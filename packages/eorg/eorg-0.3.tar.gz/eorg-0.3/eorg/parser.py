import re
from eorg.const import TOKENS, METADATA, ESCAPE


class Token:
    __slots__ = ["token", "value", "attrs"]

    def __init__(self, token, value="", attrs=""):
        self.token = token
        self.value = value
        self.attrs = attrs

    def __repr__(self):
        return f'Token(token="{self.token}", value="{self.value}", attrs="{self.attrs}")'


class Document:
    pos = 0
    doc = []
    index = {}

    def __init__(self):
        self.doc = []
        self.index = {}

    def __getattr__(self, name, default=None):
        idx = self.index.get(name.upper(), [])
        if not idx:
            if default is not None:
                return default
            raise AttributeError(f"Attribute of {name} does not exist in document")
        if len(idx) == 1:
            return self.doc[idx[0]].value
        return [self.doc[v].value for v in idx]

    def token(self):
        if self.doc:
            return self.doc[-1].token
        return ""

    def update(self, value):
        self.doc[-1].value += value

    def __iter__(self):
        self.pos = 0
        for item in self.doc:
            yield item
            self.pos += 1

    def previous(self, match):
        if self.pos is 0:
            return None
        if self.doc[self.pos-1].token != match:
            return None
        return self.doc[self.pos-1]

    def filter(self, value):
        """Only return types that are of intrest like source blocks"""
        for item in self.doc:
            if item.token == value:
                yield item

    def body(self):
        for item in self.doc:
            if item.token in METADATA:
                continue
            yield item

    def images(self):
        for item in self.__iter__():
            if item.token == 'IMG':
                yield item.value[0]
            if item.token == 'TEXT':
                if isinstance(item.value, list):
                    for token in item.value:
                        if token.token == 'IMG':
                            yield token

    def __len__(self):
        return len(self.doc)

    def append(self, value):
        self.index.setdefault(value.token, []).append(len(self.doc))
        self.doc.append(value)

def parse_attrs(text):
    attrs = {}
    value_list = text.split(':')
    attrs['language'] = value_list.pop(0).strip()
    for row in value_list:
        values = row.strip().split(' ')
        attrs[values[0]] = values[1:]
    return attrs

def parsebody(text, rx):
    match = re.search(rx, text)
    if match:
        return False, ""
    else:
        return rx, text + "\n"


def parseline(text):
    print(text)
    for key, (rx, block, s, e, count) in TOKENS.items():
        match = re.search(rx, text)
        if not match:
            continue
        level = len(match.group(0))
        if count is True:
            key += str(level)
        if key == "META":
            return (
                block,
                Token(token=match.group(0)[s:e], value=text[match.end() :]),
            )
        if key == "SRC_BEGIN":
            return block, Token(token=key, attrs=parse_attrs(text[match.end():]))
        return block, Token(token=key, value=text[match.end():])

    text = text.strip()
    if text == "":
        return False, Token(token="BREAK", value=text)
    return False, Token(token="TEXT", value=text + " ")


def parse_text(txt):
    char = True
    tokens = []

    def img(char, step):
        if char != '[':
            return char
        char = next(step, None)

        if char != '[':
            return char
        char = next(step, None)

        path = ''
        while char not in [']'] + ESCAPE:
            path += char
            char = next(step, None)
        char = next(step, None)

        alt = ''
        if char == '[':
            char = next(step, None)
            while char not in [']'] + ESCAPE:
                alt += char
                char = next(step, None)
            char = next(step, None)

        tokens.append(Token('IMG', [path, alt]))
        return ''

    def emphasis(char, step, end='*', tag='b'):
        if not char or char!=end:
            return char
        char = next(step, None)
        r = ''
        while char and char not in [end] + ESCAPE:
            r += char
            char = next(step, None)
        tokens.append(Token('b', r))
        return ''


    step = iter(txt)
    while char is not None:
        char = next(step, None)
        char = emphasis(char, step, '*', 'b')
        char = emphasis(char, step, '/', 'i')
        char = emphasis(char, step, '_', 'u')
        char = emphasis(char, step, '=', 'v')
        char = emphasis(char, step, '~', 'pre')
        char = img(char, step)
        if not char:
            continue
        if len(tokens) == 0:
            tokens.append(Token('TEXT', char))
            continue
        if tokens[-1].token != 'TEXT':
            tokens.append(Token('TEXT', char))
            continue
        tokens[-1].value += char
    return tokens


def parse(stream):
    doc = Document()
    block = False
    for line in stream:
        line = line.strip()
        if block is not False:
            result = parsebody(line, block)
            if result:
                block = result[0]
                doc.update(result[1])
                continue
        result = parseline(line)
        if result:
            block = result[0]
            if doc.token() == "TEXT" and result[1].token == "TEXT":
                doc.update(result[1].value)
                continue
            doc.append(result[1])

    for item in doc.filter('TEXT'):
        #print('@@@@@@@@@@@@@@@@@')
        #print(item.value)
        item.value = parse_text(item.value)
    return doc
