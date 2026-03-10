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

    @staticmethod
    def tokenize(code: str) -> list[Token]:
        pass

data = open("../tests/helloworld.print", 'r', encoding='utf-8').read()

for token in Tokenizer.tokenize(data):
    print(token.token_type.name, token.value, token.int_value)