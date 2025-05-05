from dataclasses import dataclass

@dataclass
class Node:
    def __init__(self, kind, l, r=None, annotated_type=None):
        self.__kind = kind
        self.__lhs = l
        self.__rhs = r
        self.__type = annotated_type

    def get_kind(self):
        return self.__kind

    def get_lhs(self):
        return self.__lhs

    def get_rhs(self):
        return self.__rhs

    def get_type(self):
        return self.__type