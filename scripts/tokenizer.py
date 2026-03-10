from token import Token, TokenType
from position import PositionRange

KEYWORDS = {
        "čo ak": "if",
        "ibaže": "elif",
        "inak": "else",
        "kým platí, že": "while",
        "pre každé": "for",
        "trieda": "class",
        "definuje": "def",
        "skús": "try",
        "okrem": "except",
        "na koniec": "finally",
        "in": "v",
        "sa rovná": "==",
        "je menšie ako": "<",
        "je väčšie ako": ">",
        "je menšie alebo rovné ako": "<=",
        "je väčšie alebo rovné ako": ">=",
        "sa nerovná": "!=",
        "neplatí": "not",
        "alebo": "or",
        "a": "and",
        "je": "is",
        "definuj": "def",
        "zmaž": "del",
        "vráť": "return",
        "výnos": "yield",
        "ako": "as",
        "importuj": "import",
        "z": "from",
        "zlom": "break",
        "pokračuj": "pass",
        "preskoč": "continue",
        "klamstvo": "False",
        "pravda": "True",
        "nič": "None",
        "verejné": "global",
        "nelokálna": "nonlocal",
        "využi": "with",
        "porovnaj": "match",
        "v prípade, že": "case",
        "vyvráť": "raise",
        "skrátená funkcia, väčšinou anonymná a bez mena, používa sa pri krátkych operáciach alebo vo vnútri funkcií ako argument": "lambda"
    }

class Tokenizer:

    curr_token: Token = Token()
    result: list[Token] = []
    is_string = False
    is_comment = False
    position: PositionRange = PositionRange()
    curr_line: list[Token] = []

    @staticmethod
    def tokenize(code: str) -> list[Token]:

        curr_token = Token(token_type=TokenType.INDENT)
        result: list[Token] = Tokenizer.result

        for char in code:
            if char == " ":
                Tokenizer.tokenize_space()
            elif char == "\n":
                Tokenizer.tokenize_end_line()
            elif char == ",":
                Tokenizer.curr_token.token_type = TokenType.ARGUMENT
                Tokenizer.curr_token.add_to_value(char)
            elif char == "=":
                Tokenizer.add_token(Tokenizer.curr_token)
                Tokenizer.add_token(Token(token_type=TokenType.OPERATION, value="="))
                Tokenizer.curr_token = Token(token_type=TokenType.VALUE)
            elif Tokenizer.curr_token.token_type.is_indent_next:
                Tokenizer.add_token(Tokenizer.curr_token)
                Tokenizer.curr_token = Token(token_type=TokenType.UNKNOWN, value=char)
            else:
                Tokenizer.curr_token.add_to_value(char)

        return result

    @staticmethod
    def get_latest_unknowns() -> list[Token]:
        result = []
        for t in Tokenizer.curr_line:
            if t.token_type == TokenType.UNKNOWN:
                result.append(t)
            else:
                result = []
        return result

    @staticmethod
    def join_values(t: list[Token]) -> str:
        return " ".join(i.value for i in t)

    @staticmethod
    def add_token(t: Token) -> None:
        Tokenizer.result.append(t)
        Tokenizer.curr_line.append(t)

    @staticmethod
    def tokenize_end_line() -> None:
        Tokenizer.result.append(Tokenizer.curr_token)

        if Tokenizer.curr_token.value.endswith(("!", "?", ".")):
            char = Tokenizer.curr_token.remove_from_value(1)
            Tokenizer.add_token(Token(token_type=TokenType.KEYWORD_LINE_END, value=char))

        Tokenizer.curr_token = Token(token_type=TokenType.NEW_LINE, value="\n")
        Tokenizer.curr_line = []


    # run away as fast as you can
    @staticmethod
    def tokenize_space() -> None:

        if Tokenizer.curr_token.token_type.is_indent_next:
            if Tokenizer.curr_token.token_type == TokenType.INDENT:
                Tokenizer.curr_token.int_value += 1
            else:
                Tokenizer.add_token(Tokenizer.curr_token)
                Tokenizer.curr_token = Token(TokenType.INDENT)

        elif Tokenizer.is_string or Tokenizer.is_comment:
            Tokenizer.curr_token.add_to_value(" ")

        elif Tokenizer.curr_token.token_type == TokenType.KEYWORD:
            Tokenizer.add_token(Tokenizer.curr_token)
            Tokenizer.curr_token = Token()

        elif Tokenizer.curr_token.token_type == TokenType.ARGUMENT:
            Tokenizer.curr_token.add_to_value(" ")

        elif Tokenizer.curr_token.token_type == TokenType.UNKNOWN:
            if Tokenizer.curr_token.value in KEYWORDS:
                Tokenizer.curr_token.token_type = TokenType.KEYWORD
                Tokenizer.add_token(Tokenizer.curr_token)
                Tokenizer.curr_token = Token()
            else:
                Tokenizer.curr_token.token_type = TokenType.VALUE
                Tokenizer.add_token(Tokenizer.curr_token)
                Tokenizer.curr_token = Token()
data = open("../tests/helloworld.print", 'r', encoding='utf-8').read()

for token in Tokenizer.tokenize(data):
    print(token.token_type.name, token.value, token.int_value)