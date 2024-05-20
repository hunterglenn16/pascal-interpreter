# Token types
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance_token(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def whitespace_skip(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance_token()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance_token()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        if self.current_char is not None:

            if self.current_char.isspace():
                self.whitespace_skip()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance_token()
                return Token(PLUS, self.current_char)

            if self.current_char == '-':
                self.advance_token()
                return Token(MINUS, self.current_char)

            if self.current_char == '*':
                self.advance_token()
                return Token(MULTIPLY, self.current_char)

            if self.current_char == '/':
                self.advance_token()
                return Token(DIVIDE, self.current_char)

            self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MULTIPLY:
            self.eat(MULTIPLY)
        elif op.type == DIVIDE:
            self.eat(DIVIDE)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == MULTIPLY:
            result = left.value * right.value
        elif op.type == DIVIDE:
            result = left.value / right.value
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
