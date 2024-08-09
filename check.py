INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"


class Token(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        return SyntaxError("Error with parsing")

    def advance(self):
        if self.current_char is not None:
            self.pos += 1

    def integer(self):
        result = ""
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def get_token(self):
        if self.current_char:

            if self.current_char.isspace():
                self.advance()

            if self.current_char.isdigit():
                return Token(self.integer(), INTEGER)

            if self.current_char == "+":
                self.advance()
                return Token("+", PLUS)

            if self.current_char == "-":
                self.advance()
                return Token("-", MINUS)

        return (None, EOF)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_token()

    def eat(self, type):
        if self.current_token.type == type:
            ...

    def expr(self):
        ...


def main():
    text = input("> ")
    lexer = Lexer(text)
    interpreter = Interpreter(Lexer)


if __name__ == "__main__":
    main()
