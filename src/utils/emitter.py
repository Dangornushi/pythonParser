import os


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


class RustEmitter(BaseEmitter):
    """Currently identical to BaseEmitter but exists for language-specific
    customizations later.
    """
    pass
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
