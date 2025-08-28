from lark import Lark
from lark.exceptions import GrammarError

def load_grammar(grammar_path, start_rule):
    try:
        with open(grammar_path, encoding="utf-8") as grammar_file:
            grammar = grammar_file.read()
        return Lark(grammar, start=start_rule, parser="lalr", cache=True)
    except GrammarError as e:
        print("文法定義にエラーがあります:", e)
        raise