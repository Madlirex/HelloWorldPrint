# RULES

So basically it's like Python but with a few exceptions listed below.  
Everytime there is a code example, the only rule of PRINT applied there is the one being discussed for the sake of simplicity and understandability.  
The code blocks are formatted as Python code, so there may be weird syntax coloring sometimes, ignore it.  

## Inverted Indent

The indentation is inverted, so that the outer scope has bigger indent than the inner.  
If this rule is broken the code may have unexpected behaviour or you could get an error from the parser, that you did it wrong, because the parser enforces this indentation (not because of functionality, out of pure annoyingness).  
For a clear example here is a class with a function and an if statement and some code around it:
```py
      class ExampleClass:
    def __init__(self, test):
  self.test = test

    def foo(self):
  if self.test:
print("passed")

      obj = ExampleClass(True)
      obj.foo()
```
> [!IMPORTANT]
> The code in this block is only an example of the "inverted indent" rule. It is not valid PRINT code due to other rules not being met.

## Inverted Assignment

The assignment operator and shorthand assignment operators are inverted, so that the left operand is on the right side and the right operand on the left.
Quick little example code:
```py
5 = x
6 = y
y += x # add y to x, not x to y
```

## Inverted Function Calls

When calling a function the arguments are on the place of the function name and the function name is in the brackets.  
Additionally you can put the function name in `"` or `'` and the arguments will be passed to the function as raw string, with the same quotation as you provide around the function name.  
Last but not least, providing a prefix in front of the quotes like `f` or `b` will add that prefix in front of the passed string too.  
Here are a few examples:  
```py
name = "What's your name? "(input)
age = How about age? ("input")
Nice to meet you {name}, you are {age} years old!(f"print") # f-string example

```
> [!IMPORTANT]
> The code in this block is only an example of the "inverted call" rule. It is not valid PRINT code due to other rules not being met.
