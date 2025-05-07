#Ricardo Hespanhol Pamplona

import sys

class Lexer:
    def __init__(self, text):
        # Initialize lexer with input text
        self.text = text          # The input text to tokenize
        self.pos = 0              # Current position in the text
        self.current_char = self.text[self.pos] if self.text else None  # Current character being processed
        self.line = 1             # Current line number (for error reporting)
        self.column = 1           # Current column number (for error reporting)
        self.current_state = "S0" # Current state of the lexer (state machine)
        self.buffer = ""          # Buffer to accumulate token characters
        self.start_pos = (self.line, self.column)  # Starting position of current token

    def advance(self):
        # Move to the next character in the input
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            self.column += 1
        else:
            self.current_char = None  # End of input

    def reset_state(self):
        # Reset the lexer to initial state
        self.current_state = "S0"
        self.buffer = ""
        self.start_pos = (self.line, self.column)

    def get_next_token(self):
        # Main method to get the next token from input
        while self.current_char is not None:
            if self.current_state == "S0":
                token = self.state_S0()
                if token: return token
            elif self.current_state == "S1":
                token = self.state_S1()
                if token: return token
            elif self.current_state == "S2":
                token = self.state_S2()
                if token: return token
            elif self.current_state == "S3":
                token = self.state_S3()
                if token: return token
            elif self.current_state == "S4":
                token = self.state_S4()
                if token: return token
            elif self.current_state == "S5":
                self.state_S5()
        return None  # No more tokens

    # ---------------------------------------------
    # S0: Initial State - decide what type of token we're starting
    # ---------------------------------------------
    def state_S0(self):
        self.start_pos = (self.line, self.column)
        self.buffer = ""

        # Parentheses
        if self.current_char in '()':
            token_type = 'PARENTESE_ABRE' if self.current_char == '(' else 'PARENTESE_FECHA'
            token = (token_type, self.current_char, self.start_pos)
            self.advance()
            return token

        # Operators
        elif self.current_char in '+-*/|%^<>=':
            self.current_state = "S3"
            self.buffer = self.current_char
            self.advance()
            return None

        # Numbers (digits or starting with decimal point)
        elif self.current_char.isdigit() or self.current_char == '.':
            self.current_state = "S1"
            self.buffer += self.current_char
            self.advance()
            return None

        # Identifiers (start with letter)
        elif self.current_char.isalpha():
            self.current_state = "S2"
            self.buffer += self.current_char
            self.advance()
            return None

        # Whitespace
        elif self.current_char.isspace():
            self.advance()
            return None

        # Invalid character
        else:
            raise Exception(f"Invalid character: '{self.current_char}' (line {self.line}, column {self.column})")

    # ---------------------------------------------
    # S1: Processing Numbers (integers or decimals)
    # ---------------------------------------------
    def state_S1(self):
        # Check for invalid second decimal point
        if self.current_char == '.' and '.' in self.buffer:
            raise Exception(f"Invalid number: '{self.buffer}.' (line {self.start_pos[0]}, column {self.start_pos[1]})")
            
        # Add decimal point or digit to number buffer
        if self.current_char == '.':
            self.buffer += self.current_char
            self.advance()
            return None
        elif self.current_char.isdigit():
            self.buffer += self.current_char
            self.advance()
            return None
        else:
            # Check for trailing decimal point
            if self.buffer.endswith('.'):
                raise Exception(f"Invalid number: '{self.buffer}' (line {self.start_pos[0]}, column {self.start_pos[1]})")
            # Return the completed number token
            token = ('NUMERO', self.buffer, self.start_pos)
            self.reset_state()
            return token

    # ---------------------------------------------
    # S2: Processing Identifiers or Keywords
    # ---------------------------------------------
    def state_S2(self):
        # Continue accumulating identifier characters
        if self.current_char.isalpha():
            self.buffer += self.current_char
            self.advance()
            return None
        else:
            # Check if identifier is a command or keyword
            if self.buffer in ['RES', 'MEM']:
                token = ('COMANDO', self.buffer, self.start_pos)
            elif self.buffer in ['if', 'then', 'else', 'for']:
                token = ('PALAVRA_CHAVE', self.buffer, self.start_pos)
            else:
                token = ('VARIAVEL', self.buffer, self.start_pos)
            self.reset_state()
            return token

    # ---------------------------------------------
    # S3: Processing Operators (single-character)
    # ---------------------------------------------
    def state_S3(self):
        # Return the operator token
        token = ('OPERADOR', self.buffer, self.start_pos)
        self.reset_state()
        return token

    # ---------------------------------------------
    # S4: Decimal Point State 
    # ---------------------------------------------
    def state_S4(self):
        pass 

    # ---------------------------------------------
    # S5: Double decimal point
    # ---------------------------------------------
    def state_S5(self):
        raise Exception(f"Invalid number: '{self.buffer}' (line {self.start_pos[0]}, column {self.start_pos[1]})")

if __name__ == "__main__":
    # Command line interface
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <test_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)

    lexer = Lexer(code)
    
    try:
        # Tokenize the input and print each token
        while True:
            token = lexer.get_next_token()
            if token is None: break
            print(f"{token[0]:<15} | Value: {token[1]:<6} | Position: {token[2]}")
    except Exception as e:
        print(f"\nError during lexical analysis:\n{e}")
        sys.exit(1)