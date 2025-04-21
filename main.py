#!/usr/bin/env python3
import sys
from lark import Lark
from lark import Transformer
from lark.exceptions import UnexpectedInput
from lark.exceptions import GrammarError
from functools import reduce
from dataclasses import dataclass

@dataclass
class Memory:
    def __init__(self):
        self.kind = ""
        self.name = None
        self.variable = None

    def set(self, kind, name, variable):
        self.kind = kind
        self.name = name
        self.variable = variable

@dataclass
class Node:
    def __init__(self, kind, l, r=None):
        self.kind = kind
        self.lhs = l
        self.rhs = r

    def get_kind(self):
        return self.kind

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

# 構文解析器の実行部
class CalcTransformer(Transformer):
    def function(self, tree):
        function_name = tree[0]
        function_body = [tree[i] for i in range(1, len(tree))]
        return Node("FUNCTION", function_name, function_body)

    def statement(self, tree):
        return Node("STATEMENT", tree[0])

    def let(self, tree):
        if len(tree) > 1:
            return Node("LET", tree[0], tree[1])
        return tree[0]

    def loop(self, tree):
        return Node("LOOP", tree[0])

    def if_stmt(self, tree):
        return Node("IF", tree[0], tree[1])

    def while_stmt(self, tree):
        return Node("WHILE", tree[0], tree[1])

    def for_stmt(self, tree):
        return Node("FOR", tree[0], tree[1])

    def match_stmt(self, tree):
        return Node("MATCH", tree[0], tree[1])

    def expr(self, tree):
        if len(tree) > 1:
            return Node("EXPR", tree[0], tree[1])
        return tree[0]

    def term(self, tree):
        if len(tree) > 1:
            return Node("TERM", tree[0], tree[1])
        return tree[0]

    def factor(self, tree):
        return Node("FACTOR", tree[0])

    def number(self, tree):
        return Node("NUM", tree[0])

    def string(self, tree):
        return Node("STR", tree[0])


def printNode(node, callCount=0):
    callCount += 1
    print(node.get_kind())

    if type(node.get_lhs()) == Node and node.get_kind() == "FUNCTION":
        for i in range(node.get_rhs().__len__()):
            printNode(node.get_rhs()[i])

    else:
        if type(node.get_lhs()) == Node:
            for i in range(callCount):
                print("  ", end="")
            print("L: ", end="")
            printNode(node.get_lhs(), callCount)
        elif node.get_lhs() is not None:
            for i in range(callCount):
                print("  ", end="")
            print("L: ", node.get_lhs())

        if type(node.get_rhs())== Node:
            for i in range(callCount):
                print("  ", end="")
            print("R: ", end="")
            printNode(node.get_rhs(), callCount)
        elif node.get_rhs() is not None:
            for i in range(callCount):
                print("  ", end="")
            print("R: ", node.get_rhs())

    callCount -= 1

args = sys.argv

try:
    grammar = open("./calc_grammar.lark", encoding="utf-8")
    parser = Lark(grammar.read(), start="function", parser="lalr")
except GrammarError as e:
    print("文法定義にエラーがあります:", e)
    sys.exit(1)  # エラーが致命的な場合はプログラムを終了

text = open("./test.rs", encoding="utf-8", mode="r").read()

try:
    tree = parser.parse(text)
    result = CalcTransformer().transform(tree)
    print("result")
    printNode(result)
except UnexpectedInput as e:
    print(f"エラー位置: {e.line}:{e.column}")  # 行と列
    print(f"エラー周辺のテキスト:\n{e.get_context(text)}")  # エラー周辺のテキスト