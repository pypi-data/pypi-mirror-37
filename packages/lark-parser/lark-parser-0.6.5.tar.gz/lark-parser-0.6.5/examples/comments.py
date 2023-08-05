from lark import Lark

parser = Lark(r"""
    start: command*

    command: "command"i INT
           | "block"i "{" command* "}"

    COMMENT: /#.*\n/

    %import common (INT, WS)
    %ignore WS
    %ignore COMMENT
""")

example_text = """
# Comment for command 1
Command 1

# Comment for block
Block {
    Command 2   # Inline comment for command 2
    Command 3   # Inline comment for command 3

    # Comment for command 4
    Command 4
}

"""

print(parser.parse(example_text).pretty())