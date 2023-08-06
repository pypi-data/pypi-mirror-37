from io import StringIO
from eorg.const import Token, ESCAPE
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def src(doc, code, cls=''):
    lexer = get_lexer_by_name(code.attrs.get('language', 'shell'))
    return highlight(code.value, lexer, HtmlFormatter())

def img(doc, item, cls=''):
    caption = doc.previous('CAPTION')
    text = ''
    if caption:
        text = f'<p class="center-align">{caption.value}</p>'
    return f'<img{cls} style="margin:auto;" src="{item.value[0]}" alt="{item.value[1]}" />{text}'


def parse_text_html(doc, token, cls=''):
    if isinstance(token.value, list):
        for item in token.value:
            return handle_token(doc, item)
    return f'<p{cls}>{token.value}</p>'

builddoc ={
    "HEADER1": ("h2", None),
    "HEADER2": ("h3", None),
    "HEADER3": ("h4", None),
#    "BREAK": "br",
    "IMG": (img, 'materialboxed center-align responsive-img'),
    "B": ("b", None),
    "U": ("u", None),
    "i": ("i", None),
    "TEXT": (parse_text_html, "flow-text"),
    "SRC_BEGIN": (src, None),
    "EXAMPLE": ('blockquote', None),
}

def handle_token(doc, item):
    response = StringIO()
    match = builddoc.get(item.token)
    if not match:
        return ''
    tag, cls = match
    if cls:
        cls = f' class="{cls}"'
    else:
        cls = ''
    if callable(tag):
        return tag(doc, item, cls)
    else:
        return '<%s%s>%s</%s>\n' % (tag, cls, item.value, tag)


def html(doc):
    response = StringIO()
    for item in doc:
        response.write(handle_token(doc, item))
    response.seek(0)
    return response
