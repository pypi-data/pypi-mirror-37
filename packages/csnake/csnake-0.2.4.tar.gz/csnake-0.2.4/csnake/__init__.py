# -*- coding: utf-8 -*-
from ._version import get_versions
from .cconstructs import AddressOf
from .cconstructs import Arrow
from .cconstructs import Dereference
from .cconstructs import Dot
from .cconstructs import Enum
from .cconstructs import FormattedLiteral
from .cconstructs import FuncPtr
from .cconstructs import Function
from .cconstructs import GenericModifier
from .cconstructs import OffsetOf
from .cconstructs import simple_bool_formatter
from .cconstructs import simple_str_formatter
from .cconstructs import Struct
from .cconstructs import Subscript
from .cconstructs import TextModifier
from .cconstructs import Typecast
from .cconstructs import Variable
from .cconstructs import VariableValue
from .codewriter import CodeWriter

__version__ = get_versions()["version"]
del get_versions

__all__ = (
    "CodeWriter",
    "Enum",
    "Struct",
    "Function",
    "Variable",
    "FuncPtr",
    "FormattedLiteral",
    "VariableValue",
    "AddressOf",
    "Arrow",
    "Dereference",
    "Dot",
    "GenericModifier",
    "OffsetOf",
    "Subscript",
    "TextModifier",
    "Typecast",
    "pil_converter",
    "simple_bool_formatter",
    "simple_str_formatter",
    "__version__",
)
