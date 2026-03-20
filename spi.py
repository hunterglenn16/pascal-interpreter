
from token import TokenType


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'PROGRAM': Token(TokenType.PROGRAM, 'PROGRAM'),
    'VAR': Token(TokenType.VAR, 'VAR'),
    'DIV': Token(TokenType.INTEGER_DIV, 'DIV'),
    'INTEGER': Token(TokenType.INTEGER, 'INTEGER'),
    'REAL': Token(TokenType.REAL, 'REAL'),
    'BEGIN': Token(TokenType.BEGIN, 'BEGIN'),
    'END': Token(TokenType.END, 'END'),
    'PROCEDURE': Token(TokenType.PROCEDURE, "PROCEDURE")
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token = Token('REAL_CONST', float(result))

        else:
            token = Token('INTEGER_CONST', int(result))

        return token

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def error(self):
        raise Exception("Error parsing input")

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token = RESERVED_KEYWORDS.get(result.upper(), Token(TokenType.ID, result))
        return token

    def get_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char is not None and (self.current_char.isalpha() or self.current_char == "_"):
                return self._id()

            if self.current_char is not None and self.current_char.isdigit():
                return self.number()

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ":=")

            if self.current_char == ";":
                self.advance()
                return Token(TokenType.SEMI, ";")

            if self.current_char == ".":
                self.advance()
                return Token(TokenType.DOT, ".")

            if self.current_char == ":":
                self.advance()
                return Token(TokenType.COLON, ":")

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ",")

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MULTIPLY, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.FLOAT_DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAR, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAR, ")")

            self.error()

        return Token(TokenType.EOF, None)


class AST(object):
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDec(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class ProcedureDec(AST):
    def __init__(self, proc_name, block_node):
        self.proc_name = proc_name
        self.block_node = block_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

    def error(self):
        raise Exception('Invalid Syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_token()

        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)
        elif token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        elif token.type == TokenType.LPAR:
            self.eat(TokenType.LPAR)
            node = self.expr()
            self.eat(TokenType.RPAR)
            return node
        else:
            node = self.variable()
            return node

    def program(self):
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        program_name = var_node.value
        self.eat(TokenType.SEMI)
        block_node = self.block()
        program_node = Program(program_name, block_node)
        self.eat(TokenType.DOT)
        return program_node

    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_nodes = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_nodes)
        return node

    def declarations(self):
        declarations = []
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_dec1 = self.variable_declarations()
                declarations.extend(var_dec1)
                self.eat(TokenType.SEMI)

        while self.current_token.type == TokenType.PROCEDURE:
            self.eat(TokenType.PROCEDURE)
            proc_name = self.current_token.value
            self.eat(TokenType.ID)
            self.eat(TokenType.SEMI)
            block_node = self.block()
            proc_dec1 = ProcedureDec(proc_name, block_node)
            declarations.append(proc_dec1)
            self.eat(TokenType.SEMI)

        return declarations

    def variable_declarations(self):
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()
        var_declarations = [
            VarDec(var_node, type_node)
            for var_node in var_nodes
        ]

        return var_declarations

    def type_spec(self):
        token = self.current_token
        if self.current_token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        else:
            self.eat(TokenType.REAL)

        node = Type(token)
        return node

    def compound_statement(self):
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for n in nodes:
            root.children.append(n)
        return root

    def statement_list(self):
        node = self.statement()
        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            return self.error()
        return results

    def statement(self):
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self):
        return NoOp()

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV):

            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)

            node = BinOp(node, token, self.factor())
        return node

    def expr(self):

        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            if token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(node, token, self.term())
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error()

        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f'<{self.__class__.__name__} (name={self.name}, type={self.type})>'

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        symtab_header = "Symbol Table Contents"

        lines = ['\n', symtab_header, "\n", '_' * len(symtab_header), '\n']
        lines.extend(
            ('%7s : %r' % (key, value))
            for key, value in self._symbols.items()

        )
        lines.append('\n')
        string_list = '\n'.join(lines)
        return string_list

    __repr__ = __str__

    def insert(self, symbol):
        print(f"Insert: {symbol.name}")
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print(f'Lookup: {name}')
        symbol = self._symbols.get(name)
        return symbol


class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_VarDec(self, node):
        type_name = node.type_node.value
        type_symbol = self.symbol_table.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        self.symbol_table.insert(var_symbol)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)

        if var_symbol is None:
            raise NameError(f"Error: Symbol not found {var_name}")

    def visit_ProcedureDec(self, node):
        pass


class Interpreter(NodeVisitor):

    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_MEMORY = {}

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDec(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TokenType.PLUS:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.GLOBAL_MEMORY[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_MEMORY.get(var_name)

        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_ProcedureDec(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''

        return self.visit(tree)


def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symbol_table_builder = SymbolTableBuilder()
    symbol_table_builder.visit(tree)

    print('symbol table contents:')
    print(symbol_table_builder.symbol_table)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print('Run-time GLOBAL_MEMORY contents:')
    for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
        print(f'{k} = {v}')


if __name__ == "__main__":
    main()
