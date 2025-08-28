# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
指示に対しては常に日本語で回答するようにしなさい。
処理を実装する際は、その都度不要なコードが存在しないようリファクタリングしながら進めること。
新しく機能を実装し、README.mdやrequirements.txtなどに書き込む必要がある場合は忘れずに書き込むこと。

## Running the Project

- Execute the main program: `python main.py`
- The project reads `tests/test.rs` file by default and executes the Rust-like code
- Currently type checking is disabled (line 64 in main.py), enabled by changing `match True:` to `match eval.evaluate():`

## High-Level Architecture

This is a Rust-like language parser and interpreter built with Python and Lark. The codebase follows a multi-stage compilation pipeline:

### Core Pipeline Flow
1. **Grammar Parsing** (`grammar/calc_grammar.lark` → `src/parser/grammar_loader.py`): Lark grammar defines Rust-like syntax
2. **AST Transformation** (`src/parser/calc_transformer.py`): Converts Lark parse tree to custom Node-based AST
3. **Type Checking** (`src/interpreter/eval.py`): Static type analysis (currently disabled)
4. **Interpretation** (`src/interpreter/interpreter.py`): Executes the AST with runtime variable/function management

### Key Components

**Node System** (`src/ast/node.py`): Simple AST node with kind, left-hand side, right-hand side, and type annotation. All language constructs are represented as Nodes.

**Memory Management** (`src/interpreter/interpreter.py`): 
- `VariableTable`: Function-scoped variable storage
- `Variable`: Typed variable wrapper 
- `Function`: Function definition with scope and body
- Memory is organized by function scope, with main function executed by default

**Type System** (`src/interpreter/eval.py`, `src/interpreter/interpreter.py`):
- Basic types: i32, f64, bool, String, char, unit `()`, arrays
- Type checking happens in eval.py (static analysis)
- Runtime type management in interpreter.py with Variable class

**Grammar Features** (`grammar/calc_grammar.lark`):
- Function definitions with parameters and return types
- Let bindings with optional type annotations
- Control flow: if/else, while, loop, match
- Expression precedence: logical OR → AND → equality → relational → add/sub → mul/div → unary
- Comments (line `//` and block `/* */`)

### Current State and Known Issues

**Working Features:**
- Basic parsing of functions, variables, arithmetic expressions
- Function definition and simple execution (main function only)
- Variable scoping per function
- Expression evaluation with proper precedence

**Partially Working:**
- Type checking system exists but is disabled
- Control flow statements parse but execution is incomplete
- Function calls with arguments have runtime errors (src/interpreter/interpreter.py:256)

**Implementation Notes:**
- The interpreter currently only executes the main function automatically
- Variable resolution uses tuple-based identifiers: `(name, "identifier")`
- Function arguments are parsed but argument passing/parameter binding is broken
- Memory management uses a complex nested table structure that may have inconsistencies

### Architecture Decision Points

The codebase separates concerns between parsing (Lark → Node transformation) and execution (interpretation), but type checking is implemented as a separate pass rather than integrated into the interpreter. The Node structure is generic, handling all language constructs with the same three-field pattern (kind, lhs, rhs).

Variable and function storage uses a function-scoped approach where each function gets its own variable table, but the implementation has some complexity around accessing variables across scopes that may cause issues.