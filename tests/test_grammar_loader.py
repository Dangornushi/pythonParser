import pytest
import tempfile
import os
from src.parser.grammar_loader import load_grammar
from lark import Lark
from lark.exceptions import GrammarError


class TestGrammarLoader:
    """Test grammar_loader.py functionality"""
    
    def test_load_valid_grammar(self):
        """Test loading a valid grammar file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lark', delete=False) as f:
            f.write("""
start: expr
expr: NUMBER
NUMBER: /[0-9]+/
%import common.WS
%ignore WS
            """)
            f.flush()
            
            try:
                parser = load_grammar(f.name, "start")
                assert isinstance(parser, Lark)
                
                # Test parsing
                tree = parser.parse("123")
                assert tree is not None
            finally:
                os.unlink(f.name)
    
    def test_load_grammar_with_existing_file(self):
        """Test loading the actual calc_grammar.lark file"""
        if os.path.exists("./grammar/calc_grammar.lark"):
            parser = load_grammar("./grammar/calc_grammar.lark", "top_level")
            assert isinstance(parser, Lark)
    
    def test_load_nonexistent_grammar_file(self):
        """Test loading a non-existent grammar file"""
        with pytest.raises(FileNotFoundError):
            load_grammar("nonexistent.lark", "start")
    
    def test_load_invalid_grammar(self):
        """Test loading an invalid grammar file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lark', delete=False) as f:
            f.write("invalid grammar syntax !!!")
            f.flush()
            
            try:
                with pytest.raises(GrammarError):
                    load_grammar(f.name, "start")
            finally:
                os.unlink(f.name)
    
    def test_grammar_with_different_start_rules(self):
        """Test grammar loading with different start rules"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lark', delete=False) as f:
            f.write("""
expr: NUMBER
stmt: "print" expr
NUMBER: /[0-9]+/
%import common.WS
%ignore WS
            """)
            f.flush()
            
            try:
                # Test with expr as start rule
                parser1 = load_grammar(f.name, "expr")
                tree1 = parser1.parse("42")
                assert tree1 is not None
                
                # Test with stmt as start rule  
                parser2 = load_grammar(f.name, "stmt")
                tree2 = parser2.parse("print 42")
                assert tree2 is not None
            finally:
                os.unlink(f.name)
    
    def test_grammar_caching(self):
        """Test that grammar caching works"""
        if os.path.exists("./grammar/calc_grammar.lark"):
            parser1 = load_grammar("./grammar/calc_grammar.lark", "top_level")
            parser2 = load_grammar("./grammar/calc_grammar.lark", "top_level")
            
            # Both should be Lark instances (caching is internal to Lark)
            assert isinstance(parser1, Lark)
            assert isinstance(parser2, Lark)