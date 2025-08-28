import sys
from pathlib import Path

# ensure project root on sys.path when run as script
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ast.node import Node
from src.utils.generator import Generator
from src.utils.emitter import PythonEmitter


def build_sample_ast():
    # build: fn main() { let x = 1 + 2; return x }
    num1 = Node("NUM", 1)
    num2 = Node("NUM", 2)
    add = Node("ADD_EXPR", num1, num2)

    id_x = Node("ID", "x")
    let_stmt = Node("LET", id_x, add)

    ret = Node("RETURN", id_x)

    func = Node("FUNCTION", Node("ID", "main"), [let_stmt, ret])

    top = Node("TOP_LEVEL", [func])
    return top


def main():
    ast = build_sample_ast()
    gen = Generator(emitter=PythonEmitter(output_dir="scripts_py"))
    gen.generate(ast, filename="example.py")
    print("Generated scripts_py/example.py")


if __name__ == '__main__':
    main()
