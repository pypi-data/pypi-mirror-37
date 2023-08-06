import os
import pytest
from eorg.parser import parse
from eorg.generate import parse_text



text = "parse image [[../../test.jpg][test]] after image"
result = "parse image <img src=\"../../test.jpg\" alt=\"test\" /> after image"
parse_text(text)

