from antlr4 import *
import sys

class CUDAParserBase(Parser):
    def __init__(self, input: TokenStream, output=sys.stdout):
        super().__init__(input, output)

    def IsPureSpecifierAllowed(self) -> bool:
        try:
            x = self._ctx # memberDeclarator
            c = x.getChild(0).getChild(0)
            c2 = c.getChild(0)
            p = c2.getChild(1)
            if p is None:
                return False
            return p.__class__.__name__ == 'ParametersAndQualifiersContext'
        except Exception:
            return False
