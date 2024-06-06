INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def error(self):
        raise Exception("Error parsing input")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_token()
        else:
            self.error()

    def get_token(self):
        while self.current_char is not None:
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            self.error()
        return Token(EOF, None)

    def expr(self):
        self.current_token = self.get_token()

        result = self.current_token.value
        self.eat(INTEGER)
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.current_token.value
                self.eat(INTEGER)
            if token.type == MINUS:
                self.eat(MINUS)
                result -= self.current_token.value
                self.eat(INTEGER)
        return result


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
