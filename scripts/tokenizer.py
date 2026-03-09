from token import Token, TokenType

class Tokenizer:

    @staticmethod
    def tokenize(code: str) -> list[Token]:

        curr_token = Token()
        curr_value = ""
        result: list[Token] = []

        for char in code:
            if char == " ":
                if curr_token.token_type.is_indent_next:
                    pass

        return result
