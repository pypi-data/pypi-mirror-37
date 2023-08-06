from io import StringIO
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

code = 'print "Hello World"'
def src(code):
    lexer = get_lexer_by_name('lisp')
    return highlight(code, lexer, HtmlFormatter())


builddoc ={
#    "TITLE": "h1",
#    "EMAIL": "h1",
#    "AUTHOR": "h1",
    "HEADER1": "h2",
    "HEADER2": "h3",
    "HEADER3": "h4",
    "BREAK": "br",
    "TEXT": "p",
    "SRC_BEGIN": src,
#    "COMMENT": "pre",
}



def generate(doc):
    response = StringIO()
    for item in doc:
        print(item)
        tag = builddoc.get(item.token)
        if not tag:
            continue
        if callable(tag):
            response.write(tag(item.value))
            continue
        else:
            response.write('<%s>%s<%s/>\n' % (tag, item.value, tag))
    response.seek(0)
    return response
