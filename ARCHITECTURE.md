# Architecture Of The Language

In this document I will try to explain and describe the processes behind the language.  
Why is this language documented so much? Because I made it as a learning project duh.

I didn't watch any tutorials, videos, didn't see no documentation or threads, forums etc. I just sat down, thought for a while how to do it and did it. There were a lot of plan changes in the middle of it, so the code and architecture may be chaotic, but it's mine.  
> [!NOTE]
> I don't guarantee that you will understand it after reading this and I SURELY do NOT think that the language is made like a normal, effective programming language.

# Table Of Contents
1. [Tokenization](#tokenizing)
2. [Parsing](#parsing)
3. [Transpiling](#transpiling)
4. [Compiling](#compiling)

## Tokenizing

First thing that happens to any .print file when its read is tokenization.  
Tokenization is a process of converting words and phrases into tokens which the parser can understand.
There are many types of tokens, you can find the list in the [Token class](scripts/tokenizing/token.py). I won't list them here since the TokenType class is basically just a list of them.

Based off of rules (aka if statements) written in the [Tokenizer class](scripts/tokenizing/tokenizer.py) the tokenizer does different things depending on the current character it's on. 
It adds all tokens it generates into a list and then returns it.
Here is an extensive list of all these things based off of the current character the tokenizer is on, have fun reading.

### New Line (\n)
Adds a Token of type NEWLINE and a Token of type INDENT with an integer value, which represents how many spaces are there (the indent).

### Space
Goes to the next character.

### Digit
Reads the number until it runs into a non-numerical character (except a dot) and adds it to the list.

### 

## Parsing

## Transpiling

## Compiling
