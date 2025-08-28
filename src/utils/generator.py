import os
from datetime import datetime

class Generator:
    def __init__(self, output_dir="scripts"):
        self.output_dir = output_dir
        self.code_lines = []
        self.indent_level = 0
        
        # scriptsディレクトリが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def _add_line(self, line):
        """インデント付きでコード行を追加"""
        indent = "    " * self.indent_level
        self.code_lines.append(indent + line)
    
    def _indent(self):
        """インデントレベルを増加"""
        self.indent_level += 1
    
    def _dedent(self):
        """インデントレベルを減少"""
        self.indent_level = max(0, self.indent_level - 1)
    
    def generate(self, node, filename=None):
        result = self._generate_node(node)
        
        # ファイル出力が指定されている場合
        if filename and self.code_lines:
            self._write_to_file(filename)
        
        return result
    
    def _generate_node(self, node):
        match node.get_kind():
            case "TOP_LEVEL":
                self._add_line("# Generated Rust-like script")
                self._add_line(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self._add_line("")
                for child in node.get_lhs():
                    self._generate_node(child)
                return "main"
            case "FUNCTION":
                function_name = self._generate_node(node.get_lhs())
                function_body = node.get_rhs()
                type_annotation = node.get_type()
                
                # 関数定義の生成
                return_type = ""
                if type_annotation:
                    return_type = f" -> {self._generate_node(type_annotation)}"
                
                self._add_line(f"fn {function_name}(){return_type} {{")
                self._indent()
                
                for stmt in function_body:
                    self._generate_node(stmt)
                
                self._dedent()
                self._add_line("}")
                self._add_line("")
                return function_name
            case "STATEMENT":
                return self._generate_node(node.get_lhs())
            case "LET":
                variable_name = self._generate_node(node.get_lhs())
                value = self._generate_node(node.get_rhs())
                self._add_line(f"let {variable_name} = {value};")
                return variable_name
            case "LOOP":
                loop_body = node.get_lhs()
                self._add_line("loop {")
                self._indent()
                for stmt in loop_body:
                    self._generate_node(stmt)
                self._dedent()
                self._add_line("}")
                return "loop"
            case "IF":
                condition = self._generate_node(node.get_lhs())
                if_body = node.get_rhs()
                self._add_line(f"if {condition} {{")
                self._indent()
                for stmt in if_body:
                    self._generate_node(stmt)
                self._dedent()
                self._add_line("}")
                return "if"
            case "WHILE":
                condition = self._generate_node(node.get_lhs())
                while_body = node.get_rhs()
                self._add_line(f"while {condition} {{")
                self._indent()
                for stmt in while_body:
                    self._generate_node(stmt)
                self._dedent()
                self._add_line("}")
                return "while"
            case "RETURN":
                if node.get_lhs():
                    return_value = self._generate_node(node.get_lhs())
                    self._add_line(f"return {return_value};")
                else:
                    self._add_line("return;")
                return "return"
            case "ADD_EXPR":
                left = self._generate_node(node.get_lhs())
                right = self._generate_node(node.get_rhs())
                return f"{left} + {right}"
            case "SUB_EXPR":
                left = self._generate_node(node.get_lhs())
                right = self._generate_node(node.get_rhs())
                return f"{left} - {right}"
            case "MUL_EXPR":
                left = self._generate_node(node.get_lhs())
                right = self._generate_node(node.get_rhs())
                return f"{left} * {right}"
            case "DIV_EXPR":
                left = self._generate_node(node.get_lhs())
                right = self._generate_node(node.get_rhs())
                return f"{left} / {right}"
            case "EXPR":
                if node.get_rhs():
                    left = self._generate_node(node.get_lhs())
                    right = self._generate_node(node.get_rhs())
                    return f"{left} {right}"
                else:
                    return self._generate_node(node.get_lhs())
            case "FACTOR":
                return self._generate_node(node.get_lhs())
            case "FUNCTION_CALL":
                function_name = self._generate_node(node.get_lhs())
                args = []
                if node.get_rhs():
                    for arg in node.get_rhs():
                        args.append(self._generate_node(arg))
                return f"{function_name}({', '.join(args)})"
            case "ARG_LIST":
                args = []
                for arg in node.get_lhs():
                    args.append(self._generate_node(arg))
                return args
            case "NUM":
                return str(node.get_lhs())
            case "FLOAT":
                return str(node.get_lhs())
            case "STR":
                return f'"{node.get_lhs()}"'
            case "BOOL":
                return str(node.get_lhs()).lower()
            case "ID":
                return str(node.get_lhs())
            case "PRIMITIVE_TYPE":
                return str(node.get_lhs())
            case _:
                return f"/* Unknown node: {node.get_kind()} */"
    
    def _write_to_file(self, filename):
        """生成されたコードをファイルに書き込み"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.code_lines))
        print(f"✅ 生成されたスクリプトを保存しました: {filepath}")
    
    def clear(self):
        """生成されたコードをクリア"""
        self.code_lines = []
        self.indent_level = 0