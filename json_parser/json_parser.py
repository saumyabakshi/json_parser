# Tokens
(
    NUMBER,
    STRING,
    LBRACE,
    RBRACE,
    LBRACKET,
    RBRACKET,
    COLON,
    COMMA,
    TRUE,
    FALSE,
    NULL,
    EOF,
) = (
    "NUMBER",
    "STRING",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "COLON",
    "COMMA",
    "TRUE",
    "FALSE",
    "NULL",
    "EOF",
)


# Token class - this defines what is the token type
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


# Lexer class- this breaks down the text into tokens and determine which token the element belongs to
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def next(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    def number(self):
        num = ""
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.next()
        return float(num)

    def string(self):
        string = ""
        self.next()  # skipping the opening quote
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.next()
        self.next()  # skipping the closing quote
        return string

    def boolean(self):
        if self.text[self.pos :].startswith("true"):
            self.next()
            self.next()
            self.next()
            self.next()
            return True
        elif self.text[self.pos :].startswith("false"):
            self.next()
            self.next()
            self.next()
            self.next()
            self.next()
            return False

    def null(self):
        if self.text[self.pos :].startswith("null"):
            self.next()
            self.next()
            self.next()
            self.next()
            return None
    
    def error(self):
        raise Exception("Invalid Syntax", self.text[self.pos :])

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return Token(NUMBER, self.number())
            elif self.current_char == '"':
                return Token(STRING, self.string())
            elif self.current_char == "{":
                self.next()
                return Token(LBRACE, "{")
            elif self.current_char == "}":
                self.next()
                return Token(RBRACE, "}")
            elif self.current_char == "[":
                self.next()
                return Token(LBRACKET, "[")
            elif self.current_char == "]":
                self.next()
                return Token(RBRACKET, "]")
            elif self.current_char == ":":
                self.next()
                return Token(COLON, ":")
            elif self.current_char == ",":
                self.next()
                return Token(COMMA, ",")
            elif self.text[self.pos :].startswith("true"):
                return Token(TRUE, self.boolean())
            elif self.text[self.pos :].startswith("false"):
                return Token(FALSE, self.boolean())
            elif self.text[self.pos :].startswith("null"):
                return Token(NULL, self.null())
            self.error()

        return Token(EOF, None)


# Parser class - this parses the tokens and creates the JSON object
class Parser:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def error(self):
        raise Exception("Invalid Syntax")

    def recur_parse(self):
        if self.current_token.type == LBRACE:
            return self.object()
        elif self.current_token.type == LBRACKET:
            return self.array()
        elif self.current_token.type == STRING:
            return self.string()
        elif self.current_token.type == NUMBER:
            return self.number()
        elif self.current_token.type == TRUE:
            return self.boolean(True)
        elif self.current_token.type == FALSE:
            return self.boolean(False)
        elif self.current_token.type == NULL:
            return self.null()

        else:
            return self.error()

    def boolean(self, val):
        if val:
            self.check(TRUE)
            return True
        else:
            self.check(FALSE)
            return False

    def null(self):
        self.check(NULL)
        return None

    def object(self):
        obj = {}
        self.check(LBRACE)
        while self.current_token.type != RBRACE:
            key = self.string()
            self.check(COLON)
            value = self.recur_parse()
            obj[key] = value
            if self.current_token.type == COMMA:
                self.check(COMMA)
                if self.current_token.type == RBRACE:
                    self.error()
        self.check(RBRACE)
        return obj

    def string(self):
        val = self.current_token.value
        self.check(STRING)
        return val

    def number(self):
        val = self.current_token.value
        self.check(NUMBER)
        return val

    def array(self):
        res = []
        self.check(LBRACKET)
        while self.current_token.type != RBRACKET:
            res.append(self.recur_parse())
            if self.current_token.type == COMMA:
                self.check(COMMA)

        self.check(RBRACKET)
        return res

    def check(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error()

    def parse(self):
        return self.recur_parse()


# Main function - this is the entry point of the program
# def main():
#     # text = input('Enter the JSON string: ')
#     lexer = Lexer(text)
#     parser = Parser(lexer)
#     obj = parser.parse()
#     print(obj)

# main()
