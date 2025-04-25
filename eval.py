from node import Node
from memory import Memory

m = {}

Types = [
    "NUM",
    "STR",
    "BOOL",
    "ANY",    
]

class Eval:
    def __init__(self, root: Node):
        self.root = root
    def __del__(self):
        print(f"型推論結果: {m}")

    def evaluate(self, node: Node=None):
        # 引数がない場合はルートノードを使用
        if node is None:
            node = self.root

        if node.get_kind() == "NUM":
            return (int(node.get_lhs()), Types[0])
        
        elif node.get_kind() == "ID":
            return (str(node.get_lhs()), Types[1])  # 変数名を返す

        elif node.get_kind() == "STR":
            return (str(node.get_lhs()), Types[1])
        
        elif node.get_kind() == "BOOL":
            return (node.get_lhs(), Types[2])

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
        
        elif node.get_kind() == "STATEMENT":
            print(f"Evaluating statement") 
            self.evaluate(node.get_lhs())

        elif node.get_kind() == "FUNCTION":
            # 関数ノードの場合、関数名とその中身を評価
            function_name =self.evaluate(node.get_lhs()) 
            print(f"Evaluating function: {function_name}")
            for stmt in node.get_rhs():
                self.evaluate(stmt)
        
        elif node.get_kind() == "ADD_EXPR":
            print("Evaluating AND expression")
            print(self.evaluate(node.get_lhs()))
            print(self.evaluate(node.get_rhs()))
            return (True, Types[0])
        
        elif node.get_kind() == "MUL_EXPR":
            print("Evaluating OR expression")            

        elif node.get_kind() == "LET":
            # 変数定義ノードの場合、変数をメモリに保存
            variable_name = self.evaluate(node.get_lhs())
            variable_value = self.evaluate(node.get_rhs())
            print(f"Variable {variable_name[0]}: {variable_value}")

            if variable_value[0] in m:
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

        else:
            raise ValueError(f"Unknown node kind: {node.get_kind()}")