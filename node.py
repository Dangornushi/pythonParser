from dataclasses import dataclass

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