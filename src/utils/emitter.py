import os
from typing import Optional, List, Any
from typing import Optional, List, Any


class BaseEmitter:
    def __init__(self, output_dir: str = "scripts"):
        self.output_dir = output_dir
        self.code_lines = []  # type: List[str]
        self.indent_level = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def add_line(self, line):
        indent = "    " * self.indent_level
        self.code_lines.append(indent + line)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)

    def write_to_file(self, filename):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.code_lines))
        print("✅ Generated script saved: {}".format(filepath))

    def clear(self):
        self.code_lines = []
        self.indent_level = 0

    # --- Language-agnostic formatting helpers (defaults produce Rust-like output) ---
    def function_def_start(self, name, return_type=""):
        self.add_line("fn {}(){} {{".format(name, return_type))
        self.indent()

    def function_def_end(self):
        self.dedent()
        self.add_line("}")
        self.add_line("")

    def let_statement(self, var_name, value):
        self.add_line("let {} = {};".format(var_name, value))

    def loop_start(self):
        self.add_line("loop {")
        self.indent()

    def loop_end(self):
        self.dedent()
        self.add_line("}")

    def if_start(self, condition):
        self.add_line("if {} {{".format(condition))
        self.indent()

    def if_end(self):
        self.dedent()
        self.add_line("}")

    def while_start(self, condition):
        self.add_line("while {} {{".format(condition))
        self.indent()

    def while_end(self):
        self.dedent()
        self.add_line("}")

    def return_statement(self, value=None):
        if value is not None:
            self.add_line("return {};".format(value))
        else:
            self.add_line("return;")

    def format_binary(self, left, op, right):
        return "{} {} {}".format(left, op, right)

    def format_function_call(self, name, args):
        return "{}({})".format(name, ', '.join(args))

    def format_literal(self, value):
        return str(value)


class RustEmitter(BaseEmitter):
    """Simple Rust-like emitter. Keeps the same behavior as the previous generator."""
    pass


class PythonEmitter(BaseEmitter):
    """Emit Python code. Overrides formatting helpers from BaseEmitter."""

    def function_def_start(self, name, return_type=""):
        self.add_line("def {}():".format(name))
        self.indent()

    def function_def_end(self):
        self.dedent()
        self.add_line("")

    def let_statement(self, var_name, value):
        self.add_line("{} = {}".format(var_name, value))

    def loop_start(self):
        self.add_line("while True:")
        self.indent()

    def loop_end(self):
        self.dedent()

    def if_start(self, condition):
        self.add_line("if {}:" .format(condition))
        self.indent()

    def if_end(self):
        self.dedent()

    def while_start(self, condition):
        self.add_line("while {}:" .format(condition))
        self.indent()

    def while_end(self):
        self.dedent()

    def return_statement(self, value=None):
        if value is not None:
            self.add_line("return {}".format(value))
        else:
            self.add_line("return")

    def format_binary(self, left, op, right):
        return "{} {} {}".format(left, op, right)

    def format_function_call(self, name, args):
        return "{}({})".format(name, ', '.join(args))

    def format_literal(self, value):
        if isinstance(value, str):
            return '"{}"'.format(value)
        return str(value)
import os
from typing import Optional, List, Any


class BaseEmitter:
    def __init__(self, output_dir: str = "scripts"):
        self.output_dir = output_dir
        self.code_lines: List[str] = []
        self.indent_level = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def add_line(self, line: str) -> None:
        indent = "    " * self.indent_level
        self.code_lines.append(indent + line)

    def indent(self) -> None:
        self.indent_level += 1

    def dedent(self) -> None:
        self.indent_level = max(0, self.indent_level - 1)

    def write_to_file(self, filename: str) -> None:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.code_lines))
        print(f"✅ Generated script saved: {filepath}")

    def clear(self) -> None:
        self.code_lines = []
        self.indent_level = 0

    # --- Language-agnostic formatting helpers (defaults produce Rust-like output) ---
    def function_def_start(self, name: str, return_type: str = "") -> None:
        self.add_line(f"fn {name}(){return_type} {{")
        self.indent()

    def function_def_end(self) -> None:
        self.dedent()
        self.add_line("}")
        self.add_line("")

    def let_statement(self, var_name: str, value: str) -> None:
        self.add_line(f"let {var_name} = {value};")

    def loop_start(self) -> None:
        self.add_line("loop {")
        self.indent()

    def loop_end(self) -> None:
        self.dedent()
        self.add_line("}")

    def if_start(self, condition: str) -> None:
        self.add_line(f"if {condition} {{")
        self.indent()

    def if_end(self) -> None:
        self.dedent()
        self.add_line("}")

    def while_start(self, condition: str) -> None:
        self.add_line(f"while {condition} {{")
        self.indent()

    def while_end(self) -> None:
        self.dedent()
        self.add_line("}")

    def return_statement(self, value: Optional[str] = None) -> None:
        if value is not None:
            self.add_line(f"return {value};")
        else:
            self.add_line("return;")

    def format_binary(self, left: str, op: str, right: str) -> str:
        return f"{left} {op} {right}"

    def format_function_call(self, name: str, args: List[str]) -> str:
        return f"{name}({', '.join(args)})"

    def format_literal(self, value: Any) -> str:
        return str(value)


class RustEmitter(BaseEmitter):
    """Simple Rust-like emitter. Keeps prior behavior."""
    pass


class PythonEmitter(BaseEmitter):
    """Emit Python code. Overrides formatting helpers from BaseEmitter."""

    def function_def_start(self, name: str, return_type: str = "") -> None:
        # Python: def name():
        self.add_line(f"def {name}():")
        self.indent()

    def function_def_end(self) -> None:
        # ensure a blank line after function
        self.dedent()
        self.add_line("")

    def let_statement(self, var_name: str, value: str) -> None:
        # assignment in Python
        self.add_line(f"{var_name} = {value}")

    def loop_start(self) -> None:
        # Python has no infinite loop keyword, use while True:
        self.add_line("while True:")
        self.indent()

    def loop_end(self) -> None:
        self.dedent()

    def if_start(self, condition: str) -> None:
        self.add_line(f"if {condition}:")
        self.indent()

    def if_end(self) -> None:
        self.dedent()

    def while_start(self, condition: str) -> None:
        self.add_line(f"while {condition}:")
        self.indent()

    def while_end(self) -> None:
        self.dedent()

    def return_statement(self, value: Optional[str] = None) -> None:
        if value is not None:
            self.add_line(f"return {value}")
        else:
            self.add_line("return")

    def format_binary(self, left: str, op: str, right: str) -> str:
        return f"{left} {op} {right}"

    def format_function_call(self, name: str, args: List[str]) -> str:
        return f"{name}({', '.join(args)})"

    def format_literal(self, value: Any) -> str:
        # ensure strings are quoted
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)



class BaseEmitter:
    def __init__(self, output_dir="scripts"):
        self.output_dir = output_dir
        self.code_lines = []
        self.indent_level = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def add_line(self, line: str):
        indent = "    " * self.indent_level
        self.code_lines.append(indent + line)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)

    def write_to_file(self, filename: str):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.code_lines))
        print(f"✅ Generated script saved: {filepath}")

    def clear(self):
        self.code_lines = []
        self.indent_level = 0

    # --- Language-agnostic formatting helpers (defaults produce Rust-like output) ---
    def function_def_start(self, name: str, return_type: str = ""):
        self.add_line(f"fn {name}(){return_type} {{")
        self.indent()

    def function_def_end(self):
        self.dedent()
        self.add_line("}")
        self.add_line("")

    def let_statement(self, var_name: str, value: str):
        self.add_line(f"let {var_name} = {value};")

    def loop_start(self):
        self.add_line("loop {")
        self.indent()

    def loop_end(self):
        self.dedent()
        self.add_line("}")

    def if_start(self, condition: str):
        self.add_line(f"if {condition} {{")
        self.indent()

    def if_end(self):
        self.dedent()
        self.add_line("}")

    def while_start(self, condition: str):
        self.add_line(f"while {condition} {{")
        self.indent()

    def while_end(self):
        self.dedent()
        self.add_line("}")

    def return_statement(self, value: Optional[str] = None):
        if value is not None:
            self.add_line(f"return {value};")
        else:
            self.add_line("return;")

    def format_binary(self, left: str, op: str, right: str) -> str:
        return f"{left} {op} {right}"

    def format_function_call(self, name: str, args: List[str]) -> str:
        return f"{name}({', '.join(args)})"

    def format_literal(self, value) -> str:
        return str(value)


class RustEmitter(BaseEmitter):
    """Currently identical to BaseEmitter but exists for language-specific
    customizations later.
    """
    pass


class PythonEmitter(BaseEmitter):
    """Emit Python code. Overrides formatting helpers from BaseEmitter."""

    def function_def_start(self, name: str, return_type: str = ""):
        # Python: def name():
        self.add_line(f"def {name}():")
        self.indent()

    def function_def_end(self):
        # ensure a blank line after function
        self.dedent()
        self.add_line("")

    def let_statement(self, var_name: str, value: str):
        # assignment in Python
        self.add_line(f"{var_name} = {value}")

    def loop_start(self):
        # Python has no infinite loop keyword, use while True:
        self.add_line("while True:")
        self.indent()

    def loop_end(self):
        self.dedent()

    def if_start(self, condition: str):
        self.add_line(f"if {condition}:")
        self.indent()

    def if_end(self):
        self.dedent()

    def while_start(self, condition: str):
        self.add_line(f"while {condition}:")
        self.indent()

    def while_end(self):
        self.dedent()

    def return_statement(self, value: Optional[str] = None):
        if value is not None:
            self.add_line(f"return {value}")
        else:
            self.add_line("return")

    def format_binary(self, left: str, op: str, right: str) -> str:
        return f"{left} {op} {right}"

    def format_function_call(self, name: str, args: List[str]) -> str:
        return f"{name}({', '.join(args)})"

    def format_literal(self, value: Any) -> str:
        # ensure strings are quoted
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)
import os
from datetime import datetime


class BaseEmitter:
    def __init__(self, output_dir="scripts"):
        self.output_dir = output_dir
        self.code_lines = []
        self.indent_level = 0
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def add_line(self, line: str):
        indent = "    " * self.indent_level
        self.code_lines.append(indent + line)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)

    def write_to_file(self, filename: str):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.code_lines))
        print(f"✅ generated script saved: {filepath}")

    def clear(self):
        self.code_lines = []
        self.indent_level = 0


class RustEmitter(BaseEmitter):
    """Simple Rust-like emitter. Keeps the same behavior as the previous generator's
    line/indent handling but is pluggable for other emitters."""
    def __init__(self, output_dir="scripts"):
        super().__init__(output_dir=output_dir)
