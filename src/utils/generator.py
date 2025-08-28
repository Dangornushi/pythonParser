import os
from datetime import datetime
from .emitter import RustEmitter


class Generator:
    def __init__(self, output_dir="scripts", emitter=None):
        self.output_dir = output_dir
        # use provided emitter or default to RustEmitter
        self.emitter = emitter or RustEmitter(output_dir=output_dir)

        # handlers dict mapping node kinds to methods
        self.handlers = {
            "TOP_LEVEL": self._handle_top_level,
            "FUNCTION": self._handle_function,
            "STATEMENT": self._handle_statement,
            "LET": self._handle_let,
            "LOOP": self._handle_loop,
            "IF": self._handle_if,
            "WHILE": self._handle_while,
            "RETURN": self._handle_return,
            "ADD_EXPR": self._handle_add_expr,
            "SUB_EXPR": self._handle_sub_expr,
            "MUL_EXPR": self._handle_mul_expr,
            "DIV_EXPR": self._handle_div_expr,
            "EXPR": self._handle_expr,
            "FACTOR": self._handle_factor,
            "FUNCTION_CALL": self._handle_function_call,
            "ARG_LIST": self._handle_arg_list,
            "NUM": self._handle_num,
            "FLOAT": self._handle_float,
            "STR": self._handle_str,
            "BOOL": self._handle_bool,
            "ID": self._handle_id,
            "PRIMITIVE_TYPE": self._handle_primitive_type,
        }

    def _add_line(self, line):
        """インデント付きでコード行を追加（emitter 経由）"""
        self.emitter.add_line(line)

    def _indent(self):
        """インデントレベルを増加（emitter 経由）"""
        self.emitter.indent()

    def _dedent(self):
        """インデントレベルを減少（emitter 経由）"""
        self.emitter.dedent()

    def generate(self, node, filename=None):
        result = self._generate_node(node)

        # ファイル出力が指定されている場合
        if filename and self.emitter.code_lines:
            self._write_to_file(filename)

        return result

    def _generate_node(self, node):
        kind = node.get_kind()
        handler = self.handlers.get(kind, self._handle_default)
        return handler(node)

    # === handlers ===
    def _handle_top_level(self, node):
        self._add_line("# Generated Rust-like script")
        self._add_line(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._add_line("")
        for child in node.get_lhs():
            self._generate_node(child)
        return "main"

    def _handle_function(self, node):
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

    def _handle_statement(self, node):
        return self._generate_node(node.get_lhs())

    def _handle_let(self, node):
        variable_name = self._generate_node(node.get_lhs())
        value = self._generate_node(node.get_rhs())
        self._add_line(f"let {variable_name} = {value};")
        return variable_name

    def _handle_loop(self, node):
        loop_body = node.get_lhs()
        self._add_line("loop {")
        self._indent()
        for stmt in loop_body:
            self._generate_node(stmt)
        self._dedent()
        self._add_line("}")
        return "loop"

    def _handle_if(self, node):
        condition = self._generate_node(node.get_lhs())
        if_body = node.get_rhs()
        self._add_line(f"if {condition} {{")
        self._indent()
        for stmt in if_body:
            self._generate_node(stmt)
        self._dedent()
        self._add_line("}")
        return "if"

    def _handle_while(self, node):
        condition = self._generate_node(node.get_lhs())
        while_body = node.get_rhs()
        self._add_line(f"while {condition} {{")
        self._indent()
        for stmt in while_body:
            self._generate_node(stmt)
        self._dedent()
        self._add_line("}")
        return "while"

    def _handle_return(self, node):
        if node.get_lhs():
            return_value = self._generate_node(node.get_lhs())
            self._add_line(f"return {return_value};")
        else:
            self._add_line("return;")
        return "return"

    def _handle_add_expr(self, node):
        left = self._generate_node(node.get_lhs())
        right = self._generate_node(node.get_rhs())
        return f"{left} + {right}"

    def _handle_sub_expr(self, node):
        left = self._generate_node(node.get_lhs())
        right = self._generate_node(node.get_rhs())
        return f"{left} - {right}"

    def _handle_mul_expr(self, node):
        left = self._generate_node(node.get_lhs())
        right = self._generate_node(node.get_rhs())
        return f"{left} * {right}"

    def _handle_div_expr(self, node):
        left = self._generate_node(node.get_lhs())
        right = self._generate_node(node.get_rhs())
        return f"{left} / {right}"

    def _handle_expr(self, node):
        if node.get_rhs():
            left = self._generate_node(node.get_lhs())
            right = self._generate_node(node.get_rhs())
            return f"{left} {right}"
        else:
            return self._generate_node(node.get_lhs())

    def _handle_factor(self, node):
        return self._generate_node(node.get_lhs())

    def _handle_function_call(self, node):
        function_name = self._generate_node(node.get_lhs())
        args = []
        if node.get_rhs():
            for arg in node.get_rhs():
                args.append(self._generate_node(arg))
        return f"{function_name}({', '.join(args)})"

    def _handle_arg_list(self, node):
        args = []
        for arg in node.get_lhs():
            args.append(self._generate_node(arg))
        return args

    def _handle_num(self, node):
        return str(node.get_lhs())

    def _handle_float(self, node):
        return str(node.get_lhs())

    def _handle_str(self, node):
        return f'"{node.get_lhs()}"'

    def _handle_bool(self, node):
        return str(node.get_lhs()).lower()

    def _handle_id(self, node):
        return str(node.get_lhs())

    def _handle_primitive_type(self, node):
        return str(node.get_lhs())

    def _handle_default(self, node):
        return f"/* Unknown node: {node.get_kind()} */"

    def _write_to_file(self, filename):
        """生成されたコードをファイルに書き込み（emitter 経由）"""
        self.emitter.write_to_file(filename)

    def clear(self):
        """生成されたコードをクリア（emitter 経由）"""
        self.emitter.clear()