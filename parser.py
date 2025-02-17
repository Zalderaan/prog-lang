from enum import Enum
from typing import Any
import math

class TokenType(Enum):
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    POWER = 'POWER'
    MODULO = 'MODULO'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    GREATER = 'GREATER'
    NUMBER = 'NUMBER'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'

class Token:
    def __init__(self, type: TokenType, value: Any, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f'Token({self.type}, {self.value}, pos={self.line}:{self.column})'

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None
        self.line = 1
        self.column = 1
        self.keywords = {'IF': TokenType.IF, 'THEN': TokenType.THEN, 'ELSE': TokenType.ELSE,
                         'AND': TokenType.AND, 'OR': TokenType.OR, 'NOT': TokenType.NOT}

    def error(self):
        raise Exception(f'Unexpected character {self.current_char} at line {self.line}, column {self.column}')

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self) -> Token:
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result), self.line, self.column - len(result))

    def _id(self) -> Token:
        result = ''
        while self.current_char and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token_type = self.keywords.get(result.upper())
        if token_type:
            return Token(token_type, result.upper(), self.line, self.column - len(result))
        self.error()

    def get_next_token(self) -> Token:
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column - 1)
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column - 1)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*', self.line, self.column - 1)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, self.column - 1)
            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POWER, '^', self.line, self.column - 1)
            if self.current_char == '%':
                self.advance()
                return Token(TokenType.MODULO, '%', self.line, self.column - 1)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column - 1)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column - 1)
            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LESS, '<', self.line, self.column - 1)
            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GREATER, '>', self.line, self.column - 1)
            self.error()
        return Token(TokenType.EOF, None, self.line, self.column)

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Expected {token_type}, got {self.current_token.type}')

    def factor(self) -> float:
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expression()
            self.eat(TokenType.RPAREN)
            return result
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return not self.factor()
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return -self.factor()
        raise Exception('Invalid factor')

    def term(self) -> float:
        result = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result *= self.factor()
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception('Division by zero')
                result /= divisor
            elif token.type == TokenType.MODULO:
                self.eat(TokenType.MODULO)
                result %= self.factor()
        return result

    def expression(self) -> float:
        return self.term()

    def parse(self):
        return self.expression()

def evaluate(text: str) -> Any:
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.parse()

def main():
    while True:
        try:
            expr = input('> ')
            if expr.lower() == 'quit':
                break
            print('Result:', evaluate(expr))
        except Exception as e:
            print('Error:', e)

if __name__ == "__main__":
    main()
