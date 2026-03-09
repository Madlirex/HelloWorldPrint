from token import Token

class Tokenizer:

    @staticmethod
    def tokenize(code: str) -> list[Token]:

        curr_token = Token()
        curr_value = ""
        result = []

        for char in code:
            pass
