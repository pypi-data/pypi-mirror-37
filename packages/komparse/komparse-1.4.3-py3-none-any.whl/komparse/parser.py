from .scanner import Scanner
from .translators import Rule
from .char_stream import StringStream

class Parser(object):
    
    def __init__(self, grammar):
        self._grammar = grammar
        self._root = Rule(self._grammar.get_root_rule())
        self._error = ""
        
    def parse(self, source):
        self._error = ""
        scanner = Scanner(StringStream(source), self._grammar)
        nodes = self._root.translate(self._grammar, scanner)
        if not scanner.has_next():
            return nodes and nodes[0] or None
        else:
            unexpected_token = scanner.peek()
            self._error = "Unexpected token: '{}' of types '{}'".format(unexpected_token.value, unexpected_token.types)
            return None
        
    def error(self):
        return self._error
