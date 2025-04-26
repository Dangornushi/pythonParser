#!/usr/bin/env python3
import sys
from lark import Lark
from lark.exceptions import UnexpectedInput, GrammarError
from memory import Memory
from node import Node
from calc_transformer import CalcTransformer
from eval import Eval

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

        if type(node.get_rhs()) == Node:
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
    eval = Eval(result)
    r = eval.evaluate()
    print(f"評価結果: {r}")

except UnexpectedInput as e:
    print(f"エラー位置: {e.line}:{e.column}")  # 行と列
    print(f"エラー周辺のテキスト:\n{e.get_context(text)}")  # エラー周辺のテキスト