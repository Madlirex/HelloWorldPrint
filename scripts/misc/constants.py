from scripts.tokenizing.token import TokenType

#region Keywords

KEYWORDS: dict[tuple[str, ...], str] = {
        ("čo", "ak"): "if",
        ("ibaže",): "elif",
        ("inak",): "else",
        ("kým", "platí", "že"): "while",
        ("pre", "každé"): "for",
        ("trieda",): "class",
        ("definuj",): "def",
        ("skús",): "try",
        ("okrem",): "except",
        ("na", "koniec"): "finally",
        ("v",): "in",
        ("sa", "rovná"): "==",
        ("je", "menšie", "ako"): "<",
        ("je", "väčšie", "ako"): ">",
        ("je", "menšie", "alebo", "rovné", "ako"): "<=",
        ("je", "väčšie", "alebo", "rovné", "ako"): ">=",
        ("sa", "nerovná"): "!=",
        ("neplatí",): "not",
        ("alebo",): "or",
        ("a",): "and",
        ("je",): "is",
        ("definuj",): "def",
        ("zmaž",): "del",
        ("vráť",): "return",
        ("výnos",): "yield",
        ("ako",): "as",
        ("importuj",): "import",
        ("z",): "from",
        ("zlom",): "break",
        ("pokračuj",): "pass",
        ("preskoč",): "continue",
        ("klamstvo",): "False",
        ("pravda",): "True",
        ("nič",): "None",
        ("verejné",): "global",
        ("nelokálna",): "nonlocal",
        ("využi",): "with",
        ("porovnaj",): "match",
        ("v", "prípade", "že"): "case",
        ("vyvráť",): "raise",
        ("skrátená", "funkcia,", "väčšinou", "anonymná", "a", "bez", "mena,", "používa", "sa", "pri", "krátkych", "operáciach", "alebo", "vo", "vnútri", "funkcií", "ako", "argument"): "lambda"
}

SWAPPED_KEYWORDS: dict[str, tuple[str, ...]] = {
    value: key for key, value in KEYWORDS.items()
}

KEYWORDS_LIST = sorted(KEYWORDS.items(), key=lambda x: -len(x[0]))

#endregion

BRACKETS: dict[str, TokenType] = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
}

BRACKET_PAIRS: dict[str, str] = {
        ")": "(",
        "]": "[",
        "}": "{"
}

OPERATORS = {
    '+', '-', '*', '**', '/', '%', '//',
    '==', '!=', '<', '<=', '>', '>=',
    '&', '|', '^', '~', '<<', '>>'
}

RENAMES = {
    "vytlač": "print",
    "vtlač": "input",
    "dĺžka": "len",
    "rozsah": "range"
}

INVALID_RENAMES = {
    value: key for key, value in RENAMES.items()
}
