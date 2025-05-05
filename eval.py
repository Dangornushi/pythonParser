from node import Node
from memory import Memory
from dataclasses import dataclass

m = {}

@dataclass
class Types:
    NUM = "number"
    FLOAT = "float"
    STR = "string"
    BOOL = "boolean"
    ID = "identifier"
    VOID = "void"

class Eval:
    def __init__(self, root: Node):
        self.root = root
        self.__now_function_type = None

    def type_error(self, value, type1, type2):
        print(f"変数{value}で型{type1}と型{type2}の不一致が発生")

    def evaluate(self, node: Node=None):
        # 引数がない場合はルートノードを使用
        if node is None:
            node = self.root

        if type(node) != Node:
            print("うまくパースできていません")
            return False

        if node.get_kind() == "TOP_LEVEL":
            for child in node.get_lhs():
                self.evaluate(child)

        elif node.get_kind() == "FUNCTION":
            # 関数ノードの場合、関数名とその中身を評価
            self.__now_function_name = self.evaluate(node.get_lhs())[0]
            self.__now_function_type = self.evaluate(node.get_type())
            m[self.__now_function_name] = self.__now_function_type
            if self.__now_function_name == "main":
                for stmt in node.get_rhs():
                    self.evaluate(stmt)

        elif node.get_kind() == "STATEMENT":
            r = self.evaluate(node.get_lhs())
            if type(r) != bool and r[0] == TypeError:
                print(f"変数{r[1]}で型{r[2][0]}と型{r[2][1]}の不一致が発生")
                return False
            return r

        elif node.get_kind() == "PRIMITIVE_TYPE":
            type_annotation = node.get_lhs()
            if type_annotation == "i32":
                return (Types.NUM)
            elif type_annotation == "f64":
                return (Types.FLOAT)
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

        elif node.get_kind() == "NUM":
            return (int(node.get_lhs()), Types.NUM)

        elif node.get_kind() == "FLOAT":
            return (float(node.get_lhs()), Types.FLOAT)

        elif node.get_kind() == "ID":
            return (str(node.get_lhs()), Types.ID)  # 変数名を返す

        elif node.get_kind() == "STR":
            return (str(node.get_lhs()), Types.STR)

        elif node.get_kind() == "BOOL":
            return (node.get_lhs(), Types.BOOL)

        elif node.get_kind() == "EXPR":
            lhs = self.evaluate(node.get_lhs())
            rhs = self.evaluate(node.get_rhs())
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

        elif node.get_kind() == "FACTOR":
            return self.evaluate(node.get_lhs())  # 再帰的に評価

        elif node.get_kind() == "FUNCTION_CALL":
            function_name = self.evaluate(node.get_lhs())
            arguments = self.evaluate(node.get_rhs())
            print(f"Evaluating function call: {function_name} with arguments {arguments}")
            if function_name[0] in m:
                function_type = m[function_name[0]]
                if function_type == Types.VOID:
                    return True
                else:
                    return (function_name[0], function_type)
            else:
                print(f"関数{function_name}は定義されていません")
                return False

        elif node.get_kind() == "ADD_EXPR":
            lhs = self.evaluate(node.get_lhs())[0]
            lhs_type = m[lhs]
            rhs_type = m[self.evaluate(node.get_rhs())[0]]
            # 型チェック
            if lhs_type == rhs_type:
                return (lhs, Types.NUM)
            else:
                self.type_error(lhs, lhs_type, rhs_type)
                return False

        elif node.get_kind() == "MUL_EXPR":
            print("Evaluating OR expression")

        elif node.get_kind() == "LET":
            # 変数定義ノードの場合、変数をメモリに保存
            variable_name = self.evaluate(node.get_lhs())
            variable_value = self.evaluate(node.get_rhs())

            if variable_value[0] == TypeError:
                return(variable_value[0], variable_name[0], (variable_value[1], variable_value[2]))

            elif variable_value[0] in m:
                m[variable_name[0]] = m[variable_value[0]]
            else:
                m[variable_name[0]] = variable_value[1]
            return variable_value

        elif node.get_kind() == "IF":
            if_condition = self.evaluate(node.get_lhs())
            print(f"Evaluating IF statement: {if_condition}")
            if_body = self.evaluate(node.get_rhs())

        elif node.get_kind() == "WHILE":
            while_condition = self.evaluate(node.get_lhs())
            print(f"Evaluating WHILE statement: {while_condition}")
            while_body = self.evaluate(node.get_rhs())

        elif node.get_kind() == "LOOP":
            print("Evaluating LOOP")
            loop_body =  self.evaluate(node.get_lhs())

        elif node.get_kind() == "RETURN":
            return_value = self.evaluate(node.get_lhs())
            if type(return_value) == bool:
                return False
            if m[return_value[0]] == self.__now_function_type:
                return True
            else:
                print(f"関数{self.__now_function_name}は型{self.__now_function_type}にも関わらず型{m[return_value[0]]}が返されました")
                return False

        else:
            raise ValueError(f"Unknown node kind: {node.get_kind()}")