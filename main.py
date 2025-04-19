#!/usr/bin/env python3
import sys
from lark import Lark
from lark import Transformer
from functools import reduce

class Memory:
    def __init__(self):
        self.kind = ""
        self.name = None
        self.variable = None

    def set(self, kind, name, variable):
        self.kind = kind
        self.name = name
        self.variable = variable
    
memory = Memory()
nodes = [] 

class Node:
    def __init__(self, kind, l, r):
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
    def number(self, tree):
        nodes.append(Node("NUM", tree[0], None))
        return tree[0]


args = sys.argv
grammar = open("./calc_grammar.lark", encoding="utf-8")
parser = Lark(grammar.read(),start="number", parser="lalr")
text = open("./test.txt", encoding="utf-8", mode="r").read()

tree = parser.parse(text)
result = CalcTransformer().transform(tree)
print("result", result)
print("result", nodes) 
