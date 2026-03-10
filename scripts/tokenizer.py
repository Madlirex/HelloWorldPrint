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

    def __init__(self) -> None:

        self.result: list[Token] = []
        self.is_comment = False
        self.is_multi_comment = False
        self.multi_comment_counter = 0
        self.is_string = False
        self.curr_token: Token = Token(token_type=TokenType.UNKNOWN)
        self.curr_line: list[Token] = []

    def tokenize(self, code: str) -> list[Token]:

        for char in code:
            pass

        return self.result

    def add_token(self, t: Token) -> None:
        pass

    def tokenize_space(self, char: str) -> None:
        pass

    def tokenize_quotes(self, char: str) -> None:
        pass

    def tokenize_new_line(self, char: str) -> None:
        pass

    def tokenize_operation(self, char: str) -> None:
        pass

    def tokenize_bracket(self, char: str) -> None:
        pass

    def tokenize_unknowns(self, tokens: list[Token]) -> None:
        pass

    def get_latest_unknowns(self) -> list[Token]:
        pass

    @staticmethod
    def join_values(tokens: list[Token]) -> str:
        pass

data = open("../tests/helloworld.print", 'r', encoding='utf-8').read()

for token in Tokenizer.tokenize(data):
    print(token.token_type.name, token.value, token.int_value)