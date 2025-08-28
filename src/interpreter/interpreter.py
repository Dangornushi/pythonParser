from ..ast.node import Node
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Types:
    NUM = "number"
    STR = "string"
    BOOL = "boolean"
    ID = "identifier"
    VOID = "void"

class Variable:
    def __init__(self, name: str, value: any, var_type: Types):
        self.__name = name
        self.__value = value
        self.__var_type = var_type
    def set_name(self, name: str):
        self.__name = name
    def get_name(self):
        return self.__name
    def get_value(self):
        return self.__value
    def get_type(self):
        return self.__var_type

class Function:
    def __init__(self, name: str, func_type: Types, args: List, body: Optional[Node], scope: Optional['VariableTable'] = None):
        self.__name = name
        self.__type = func_type
        self.__args = args
        self.__body = body
        self.__scope = scope if scope else VariableTable()

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_args(self):
        return self.__args

    def get_body(self):
        return self.__body

    def get_scope(self):
        return self.__scope

class VariableTable:
    def __init__(self):
        # 関数名をキーにして、変数の辞書を保持
        self.__table = {}

    def set_variable(self, variable: Variable, function_name: str):
        if function_name not in self.__table:
            self.__table[function_name] = {}  # 新しいスコープを作成
#        self.__table[function_name].memory[variable.get_name()] = variable
        self.__table[function_name].memory[variable.get_name()] = variable

    def get_variable(self, variable_name, function_name: str):
        if function_name in self.__table:
            table = self.__table[function_name]
            if isinstance(table, Table) and variable_name in table.memory:
                return table.memory[variable_name]
            elif isinstance(variable_name, Variable):
                return table.memory[variable_name.get_name()]
        raise KeyError(f"Variable '{variable_name}' not found in function scope '{function_name}'")

    def set_function(self, function: Function):
        if function.get_name() not in self.__table:
            self.__table[function.get_name()] = {}  # 関数スコープを初期化
        self.__table[function.get_name()] = Table(function.get_body())  # 関数スコープを設定

    def get_function_scope(self, function_name: str):
        if function_name in self.__table:
            return self.__table[function_name]
        raise KeyError(f"Function scope '{function_name}' not found")

    def get_function_block(self, function_name: str):
        if function_name in self.__table:
            return self.__table[function_name].get_body()
        raise KeyError(f"Function block '{function_name}' not found")

    def view(self):
        for function_name, variables in self.__table.items():
            print(f"Function Scope: {function_name}")
            """
            for node in variables.get_body():
                print(f"  statement: {node.get_kind()}")
            """
            for var_name, variable in variables.items():
                print(f"  Variable Name: {var_name}, Value: {variable.get_value()}, Type: {variable.get_type()}")

class Table:
    def __init__(self, body, memory=None):
        self.body = body
        self.memory = memory if memory else {}

    def get_body(self):
        return self.body

    def items(self):
        return self.memory.items()

class Interpreter:
    def __init__(self, root: Node):
        self.root = root
        self.__memory = VariableTable()
        self.__now_function_type = Types.VOID
        self.__now_function_name = None

    def execute(self, node: Node=None):
        # 引数がない場合はルートノードを使用
        if node is None:
            node = self.root

        if node.get_kind() == "TOP_LEVEL":
            for child in node.get_lhs():
                self.execute(child)
            return self.__memory

        elif node.get_kind() == "FUNCTION":
            # 関数ノードの場合、関数名とその中身を評価
            self.__now_function_name = self.execute(node.get_lhs())
            if node.get_type() is not None:
                self.__now_function_type =self.execute(node.get_type())
            self.__memory.set_function(Function(self.__now_function_name, self.__now_function_type, [], node.get_rhs()))
            if self.__now_function_name[0] == "main":
                for stmt in node.get_rhs():
                    self.execute(stmt)

        elif node.get_kind() == "STATEMENT":
            r = self.execute(node.get_lhs())
            if type(r) == tuple and r[0] == TypeError:
                print(f"変数{r[1]}で型{r[2][0]}と型{r[2][1]}の不一致が発生")
            return r

        elif node.get_kind() == "LET":
            # 変数定義ノードの場合、変数をメモリに保存
            variable_name = self.execute(node.get_lhs())
            variable_value = self.execute(node.get_rhs())
                
            if type(variable_name) == tuple:
                pass
            elif type(variable_name) == Variable:
                variable_name = variable_name.get_name()

            if type(variable_value) == tuple:
                variable_value = Variable(variable_name, variable_value[0], variable_value[1])
            elif type(variable_value) == Variable:
                variable_value.set_name(variable_name)
                print(f"変数{variable_value.get_name()}は関数{self.__now_function_name}内で宣言され値は{variable_value.get_value()}、型は{variable_value.get_type()}です")
            else:
                pass
            
            self.__memory.set_variable(variable_value, self.__now_function_name)

            return variable_value

        elif node.get_kind() == "IF":
            if_condition = self.execute(node.get_lhs())
            print(f"Evaluating IF statement: {if_condition}")
            if_body = self.execute(node.get_rhs())

        elif node.get_kind() == "WHILE":
            while_condition = self.execute(node.get_lhs())
            print(f"Evaluating WHILE statement: {while_condition}")
            while_body = self.execute(node.get_rhs())

        elif node.get_kind() == "LOOP":
            print("Evaluating LOOP")
            loop_body =  self.execute(node.get_lhs())

        elif node.get_kind() == "RETURN":
            r = self.execute(node.get_lhs())

            if type(r) == Variable:
                pass
                # print(f"変数{r.get_name()}は関数{self.__now_function_name}内で宣言され値は{r.get_value()}、型は{r.get_type()}です")
            elif r[1] == Types.ID:
                r = self.__memory.get_variable(r, self.__now_function_name)
                self.__memory.set_variable(Variable(self.__now_function_name, r.get_value(), r.get_type()), self.__now_function_name)
            return r

        elif node.get_kind() == "EXPR":
            lhs = self.execute(node.get_lhs())
            rhs = self.execute(node.get_rhs())
            if node.get_rhs() is not None:
                operator = node.get_rhs().get_kind()
                if operator == "+":
                    return lhs + rhs
                elif operator == "-":
                    return lhs - rhs
                elif operator == "*":
                    return lhs * rhs
                elif operator == "/":
                    return lhs // rhs if rhs != 0 else 0  # 整数除算
                elif operator == "%":
                    return lhs % rhs
            else:
                print(f"Evaluating expression: {lhs}")
            return lhs

        elif node.get_kind() == "ADD_EXPR":
            lhs = self.execute(node.get_lhs())
            rhs = self.execute(node.get_rhs())

            return Variable(lhs.get_name(), lhs.get_value() + rhs.get_value(), Types.NUM)

        elif node.get_kind() == "SUB_EXPR":
            lhs = self.execute(node.get_lhs())
            rhs = self.execute(node.get_rhs())

            return Variable(lhs.get_name(), lhs.get_value() - rhs.get_value(), Types.NUM)

        elif node.get_kind() == "MUL_EXPR":
            lhs = self.execute(node.get_lhs())
            rhs = self.execute(node.get_rhs())

            return Variable(lhs.get_name(), lhs.get_value() * rhs.get_value(), Types.NUM)

        elif node.get_kind() == "DIV_EXPR":
            lhs = self.execute(node.get_lhs())
            rhs = self.execute(node.get_rhs())

            return Variable(lhs.get_name(), lhs.get_value() / rhs.get_value(), Types.NUM)

        elif node.get_kind() == "FACTOR":
            return self.execute(node.get_lhs())  # 再帰的に評価

        elif node.get_kind() == "NUM":
            return Variable(node.get_lhs(), int(node.get_lhs()), Types.NUM)

        elif node.get_kind() == "FLOAT":
            return Variable(node.get_lhs(), float(node.get_lhs()), Types.NUM)

        elif node.get_kind() == "ARG_LIST":
            # 引数リストノードの場合、引数を評価
            arguments = []
            for arg in node.get_lhs():
                r = self.execute(arg)
                print(r.get_name(), r.get_value(), r.get_type())
                arguments.append(r)
            return arguments

        elif node.get_kind() == "FUNCTION_CALL":
            # Evaluate function arguments　
            parent = self.__now_function_name
            function_name = self.execute(node.get_lhs())
            arguments_stack = []

            for i in node.get_rhs():
                arguments = self.execute(i)
                print(f"arguments {arguments}")
                arguments_stack.push(arguments)
            try:
                self.__now_function_name = function_name
                body = self.__memory.get_function_block(function_name)
                result = None
                for statement in body:
                    result = self.execute(statement)

                self.__now_function_name = parent
                return result
            except KeyError:
                raise ValueError(f"Function {function_name} is not defined")

        elif node.get_kind() == "ID":
            try:
                value = self.__memory.get_variable((str(node.get_lhs()), Types.ID), self.__now_function_name)
                return value  # 変数の内容を返す
            except KeyError:
                return (str(node.get_lhs()), Types.ID)  # 変数名を返す

        elif node.get_kind() == "STR":
            return (str(node.get_lhs()), Types.STR)

        elif node.get_kind() == "BOOL":
            return (node.get_lhs(), Types.BOOL)

        elif node.get_kind() == "PRIMITIVE_TYPE":
            type_annotation = node.get_lhs()
            if type_annotation == "i32":
                return (Types.NUM)
            elif type_annotation == "f64":
                return (Types.NUM)
            elif type_annotation == "bool":
                return (Types.BOOL)
            elif type_annotation == "String":
                return (Types.STR)
            elif type_annotation == "char":
                return (Types.STR)
            elif type_annotation == "()":
                return (Types.VOID)
            elif type_annotation.startswith("[") and type_annotation.endswith("]"):
                inner_type = type_annotation[1:-1]
                return (f"[{inner_type}]")
            else:
                raise ValueError(f"Unknown type annotation: {type_annotation}")

        else:
            raise ValueError(f"Unknown node kind: {node.get_kind()}")