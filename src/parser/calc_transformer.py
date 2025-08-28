from lark import Transformer
from ..ast.node import Node

class CalcTransformer(Transformer):
    def top_level(self, tree):
        return Node("TOP_LEVEL", tree)

    def function(self, tree):
        function_name = tree[0]  # 関数名
        type_annotation = None
        function_arguments = None
        function_body = None

        index = 1
        if tree[index].get_kind() == "PARAM_LIST":
            function_arguments = tree[index]  # 関数の引数
            index += 1
        if tree[index].get_kind() == "PRIMITIVE_TYPE":
            type_annotation = tree[index] # 型宣言
            index += 1
        if tree[index].get_kind() == "STATEMENT":
            function_body = tree[index: len(tree)]  # 関数本体

        print(f"関数名: {function_name}, 引数: {function_arguments}, 型: {type_annotation}, 本体: {function_body}")
        return Node("FUNCTION", function_name, function_body, type_annotation)

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

    def match_stmt(self, tree):
        return Node("MATCH", tree[0], tree[1])

    def match_arm(self, tree):
        return Node("MATCH_ARM", tree[0], tree[1])

    def return_stmt(self, tree):
        if len(tree) > 0:
            return Node("RETURN", tree[0])
        return Node("RETURN", None)

    def expr(self, tree):
        if len(tree) > 1:
            return Node("EXPR", tree[0], tree[1])
        return tree[0]

    def and_expr(self, tree):
        if len(tree) > 1:
            return Node("AND_EXPR", tree[0], tree[1])
        return tree[0]

    def equality_expr(self, tree):
        if len(tree) > 1:
            return Node("EQUALITY_EXPR", tree[0], tree[1])
        return tree[0]

    def relational_expr(self, tree):
        if len(tree) > 1:
            return Node("RELATIONAL_EXPR", tree[0], tree[1])
        return tree[0]
 
    def add_sub_expr(self, tree):
        return tree[0]
    
    def mul_div_expr(self, tree):
        return tree[0]

    def add_expr(self, tree):
        if len(tree) > 1:
            return Node("ADD_EXPR", tree[0], tree[1])
        return tree[0]

    def sub_expr(self, tree):
        if len(tree) > 1:
            return Node("SUB_EXPR", tree[0], tree[1])
        return tree[0]

    def mul_expr(self, tree):
        if len(tree) > 1:
            return Node("MUL_EXPR", tree[0], tree[1])
        return tree[0]

    def div_expr(self, tree):
        if len(tree) > 1:
            return Node("DIV_EXPR", tree[0], tree[1])
        return tree[0]

    def unary_expr(self, tree):
        if len(tree) > 1:
            return Node("UNARY_EXPR", tree[0], tree[1])
        return tree[0]

    def factor(self, tree):
        return Node("FACTOR", tree[0])

    def function_call(self, tree):
        function_name = tree[0]
        arguments = tree[1:] if len(tree) > 1 else []
        return Node("FUNCTION_CALL", function_name, arguments)
    def param_list(self, tree):
        return Node("PARAM_LIST", tree)

    def arg_list(self, tree):
        return Node("ARG_LIST", tree)

    def annotated_type(self, tree):
        if not tree:
            print("annotated_type: tree is empty")
            return Node("TYPE", None)

        return tree[0]

    def number(self, tree):
        return Node("NUM", tree[0])

    def float(self, tree):
        return Node("FLOAT", tree[0])

    def identifier(self, tree):
        return Node("ID", tree[0])

    def string(self, tree):
        return Node("STR", tree[0])

    def boolean(self, tree):
        return Node("BOOL", tree[0])

    def primitive_i32(self, tree):
        return Node("PRIMITIVE_TYPE", "i32")

    def primitive_f64(self, tree):
        return Node("PRIMITIVE_TYPE", "f64")

    def primitive_bool(self, tree):
        return Node("PRIMITIVE_TYPE", "bool")

    def primitive_string_type(self, tree):
        return Node("PRIMITIVE_TYPE", "String")

    def primitive_char(self, tree):
        return Node("PRIMITIVE_TYPE", "char")

    def primitive_unit(self, tree):
        return Node("PRIMITIVE_TYPE", "()")

    def array_type(self, tree):
        return Node("ARRAY_TYPE", tree[0])