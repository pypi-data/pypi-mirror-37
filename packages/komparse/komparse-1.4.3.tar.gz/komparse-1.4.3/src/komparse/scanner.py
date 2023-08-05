from collections import namedtuple
from .char_stream import CharStream

Token = namedtuple('Token', 'types value')

class Scanner(object):
    
    def __init__(self, char_stream, grammar):
        self._char_stream = char_stream
        self._grammar = grammar
        self._remaining = []
        self._consumption = [[]]
        self._reader = StdReader(char_stream, self._grammar, self)
        
    def has_next(self):
        self._fill_buffer()
        return bool(self._remaining)
    
    def peek(self):
        self._fill_buffer()
        return self._remaining[-1]
    
    def advance(self):
        self._fill_buffer()
        if self._remaining:
            ret = self._remaining.pop()
            self._consumption[-1].append(ret)
            return ret
        else:
            return None
        
    def open_transaction(self):
        self._consumption.append([])
    
    def commit(self):
        if len(self._consumption) == 1:
            raise Exception("Commit not allowed")
        self._consumption[-1] +=  self._consumption.pop()
        
    def undo(self):
        if len(self._consumption) == 1:
            raise Exception("Cannot be undone")
        consumed = self._consumption.pop()
        while consumed:
            self._remaining.append(consumed.pop())
        
    def _fill_buffer(self):
        if not self._remaining:
            tokens = []
            while True:
                new_tokens = self._reader.next_tokens()
                if new_tokens is None:
                    break
                tokens += new_tokens
                if tokens:
                    break
            if tokens is not None:
                tokens.reverse()
                for token in tokens:
                    self._remaining.append(token)
        

class TokenReader(object):
    
    def __init__(self, char_stream, grammar, scanner):
        self._char_stream = char_stream
        self._grammar = grammar
        self._scanner = scanner
        self._chars = ""
        
    def next_tokens(self):
        raise NotImplementedError()
    
    def _init_chars(self, chars):
        self._chars = chars
    
    def _peek_next_char(self):
        if self._char_stream.has_next():
            return self._char_stream.peek()
        else:
            return None
        
    def _advance_char(self):
        self._chars += self._char_stream.advance()
        
    def _remove_tail(self, tail):
        self._chars = self._chars[:len(self._chars)-len(tail)]
        
    def _ends_with(self, tail):
        return self._chars[-len(tail):] == tail
        

class StdReader(TokenReader):
    
    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()
        
    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None:
                if self._chars:
                    tokens = self._create_tokens()
                    self._chars = ""
                    return tokens
                else:
                    return None
            if ch in self._wspace:
                tokens = self._create_tokens()
                self._scanner._reader = WSpaceReader(self._char_stream, self._grammar, self._scanner)
                return tokens
            self._advance_char()
            starts_comment, start, end, nestable = self._is_comment_start()
            if starts_comment:
                self._remove_tail(start)
                tokens = self._create_tokens()
                reader = CommentReader(self._char_stream, self._grammar, self._scanner)
                reader.set_delimiters(start, end, nestable)
                reader._init_chars(start)
                self._scanner._reader = reader
                return tokens
            starts_string, name, start, end, esc = self._is_string_start()
            if starts_string:
                self._remove_tail(start)
                tokens = self._create_tokens()
                reader = StringReader(self._char_stream, self._grammar, self._scanner)
                reader.set_name(name)
                reader.set_delimiters(start, end, esc)
                self._scanner._reader = reader
                return tokens
                    
    def _create_tokens(self):
        tokens = []
        remaining = self._chars
        while remaining:
            token_types, text = self._find_next_token(remaining)
            if text is not None:
                if token_types:
                    tokens.append(Token(token_types, text))
                remaining = remaining[len(text):]
            else:
                break
        if remaining:
            raise Exception("Code could not be resolved: {}".format(remaining))
        return tokens
    
    def _find_next_token(self, s):
        matches = []
        for name, regex in self._grammar.get_token_patterns():
            m = regex.match(s)
            if m:
                text = m.group(1)
                matches.append((name, text))
        return self._max_munch(sorted(matches, key=lambda it: len(it[1]), reverse=True))
        
    def _max_munch(self, sorted_matches):
        token_types = []
        max_len = None
        max_text = None
        for name, text in sorted_matches:
            if max_len is None:
                max_len = len(text)
                max_text = text
            if len(text) == max_len:
                token_types.append(name) 
            else:
                break
        return token_types, max_text
            
    def _is_comment_start(self):
        comment_delims = self._grammar.get_comments()
        for start, end, nestable in comment_delims:
            if self._ends_with(start):
                return True, start, end, nestable
        return False, None, None, False

    def _is_string_start(self):
        string_delims = self._grammar.get_strings()
        for name, start, end, esc in string_delims:
            if self._ends_with(start):
                return True, name, start, end, esc
        return False, None, None, None, None


class WSpaceReader(TokenReader):
    
    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()
        
    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None or ch not in self._wspace:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return []
            self._advance_char()


class CommentReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ""
        self._end = ""
        self._nestable = False
        
    def set_delimiters(self, start, end, nestable):
        self._start = start
        self._end = end
        self._nestable = nestable
        
    def next_tokens(self):
        nest_level = 1
        while True:
            if self._peek_next_char() is None:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return []
            self._advance_char()
            if self._ends_with(self._end):
                nest_level -= 1
                if nest_level == 0:
                    self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                    return []
            elif self._nestable and self._ends_with(self._start):
                nest_level += 1
            

class StringReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ""
        self._end = ""
        self._esc = ""
        self._name = "STRING"
        self._immut_len = 0
        
    def _ends_with(self, tail):
        mut_tail = self._chars[self._immut_len:]
        return mut_tail[-len(tail):] == tail
        
    def set_delimiters(self, start, end, esc):
        self._start = start
        self._end = end
        self._esc = esc
        
    def set_name(self, name):
        self._name = name
        
    def next_tokens(self):
        escaped_end = self._esc + self._end
        escaped_esc = 2 * self._esc
        while True:
            if self._peek_next_char() is None:
                return None
            self._advance_char()
            if self._esc and self._escape(self._end) or self._escape(self._esc):
                continue
            if self._ends_with(self._end):
                self._remove_tail(self._end)
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return [Token(types=[self._name], value=self._chars)]
            
    def _escape(self, ch):
        escaped = self._esc + ch
        if not self._ends_with(escaped):
            return False
        self._remove_tail(escaped)
        self._chars += ch
        self._immut_len = len(self._chars)
        return True
        


        
        
                    
                