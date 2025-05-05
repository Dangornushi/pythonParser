class Generator:
    def generate(self, node):
        match node.get_kind():
            case "FUNCTION":
                function_name = self.generate(node.get_lhs())
                function_body = node.get_rhs()
                print(f"Generating function: {function_name}")
                for stmt in function_body:
                    self.generate(stmt)
            case "STATEMENT":
                self.generate(node.get_lhs())
            case "LET":
                variable_name = self.generate(node.get_lhs())
                value = self.generate(node.get_rhs())
                print(f"Generating variable declaration: let {variable_name} = {value}")
            case "LOOP":
                loop_body = node.get_lhs()
                print("Generating loop:")
                for stmt in loop_body:
                    self.generate(stmt)
            case "IF":
                condition = node.get_lhs()
                if_body = node.get_rhs()
                print(f"Generating if statement with condition: {condition}")
                for stmt in if_body:
                    self.generate(stmt)
            case "WHILE":
                condition = node.get_lhs()
                while_body = node.get_rhs()
                print(f"Generating while loop with condition: {condition}")
                for stmt in while_body:
                    self.generate(stmt)
            case "RETURN":
                return_value = node.get_lhs()
                print(f"Generating return statement with value: {return_value}")
            case "EXPR":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating expression: {left} and {right}")
            case "CONDITION":
                conditions = node.get_lhs()
                print(f"Generating condition with: {conditions}")
            case "CONDITION_GREATER":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating greater-than condition: {left} > {right}")
            case "CONDITION_LESS":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating less-than condition: {left} < {right}")
            case "CONDITION_EQ":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating equality condition: {left} == {right}")
            case "CONDITION_AND":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating logical AND condition: {left} && {right}")
            case "CONDITION_OR":
                left = node.get_lhs()
                right = node.get_rhs()
                print(f"Generating logical OR condition: {left} || {right}")
            case "NUM":
                print(f"Generating number: {node.get_lhs()}")
                return node.get_lhs()
            case "STR":
                print(f"Generating string: {node.get_lhs()}")
                return node.get_lhs()
            case "CALL":
                function_name = node.get_lhs()
                print(f"Generating function call: {function_name}()")
            case _:
                raise ValueError(f"Unknown node kind: {node.get_kind()}")