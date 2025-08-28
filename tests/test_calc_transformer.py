import pytest
from lark import Tree, Token
from src.parser.calc_transformer import CalcTransformer
from src.ast.node import Node


class TestCalcTransformer:
    """Test calc_transformer.py functionality"""
    
    def setup_method(self):
        """Setup transformer for each test"""
        self.transformer = CalcTransformer()
    
    def test_top_level_transformation(self):
        """Test top_level transformation"""
        mock_tree = [Node("FUNCTION", "test")]
        result = self.transformer.top_level(mock_tree)
        
        assert isinstance(result, Node)
        assert result.get_kind() == "TOP_LEVEL"
        assert result.get_lhs() == mock_tree
    
    def test_number_transformation(self):
        """Test number transformation"""
        token = Token("NUMBER", "42")
        result = self.transformer.number([token])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "NUM"
        assert result.get_lhs() == token
    
    def test_float_transformation(self):
        """Test float transformation"""
        token = Token("FLOAT", "3.14")
        result = self.transformer.float([token])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "FLOAT"
        assert result.get_lhs() == token
    
    def test_identifier_transformation(self):
        """Test identifier transformation"""
        token = Token("IDENTIFIER", "variable_name")
        result = self.transformer.identifier([token])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "ID"
        assert result.get_lhs() == token
    
    def test_string_transformation(self):
        """Test string transformation"""
        token = Token("STRING", '"hello world"')
        result = self.transformer.string([token])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "STR"
        assert result.get_lhs() == token
    
    def test_boolean_transformation(self):
        """Test boolean transformation"""
        token = Token("BOOL", "true")
        result = self.transformer.boolean([token])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "BOOL"
        assert result.get_lhs() == token
    
    def test_primitive_type_transformations(self):
        """Test primitive type transformations"""
        # Test i32
        result = self.transformer.primitive_i32([])
        assert result.get_kind() == "PRIMITIVE_TYPE"
        assert result.get_lhs() == "i32"
        
        # Test f64
        result = self.transformer.primitive_f64([])
        assert result.get_kind() == "PRIMITIVE_TYPE"
        assert result.get_lhs() == "f64"
        
        # Test bool
        result = self.transformer.primitive_bool([])
        assert result.get_kind() == "PRIMITIVE_TYPE"
        assert result.get_lhs() == "bool"
        
        # Test String
        result = self.transformer.primitive_string_type([])
        assert result.get_kind() == "PRIMITIVE_TYPE"
        assert result.get_lhs() == "String"
    
    def test_let_transformation_with_assignment(self):
        """Test let transformation with variable assignment"""
        var_node = Node("ID", "x")
        value_node = Node("NUM", "42")
        result = self.transformer.let([var_node, value_node])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "LET"
        assert result.get_lhs() == var_node
        assert result.get_rhs() == value_node
    
    def test_let_transformation_single_element(self):
        """Test let transformation with single element"""
        var_node = Node("ID", "x")
        result = self.transformer.let([var_node])
        
        # Should return the single element
        assert result == var_node
    
    def test_add_expr_transformation(self):
        """Test add expression transformation"""
        left = Node("NUM", "5")
        right = Node("NUM", "3")
        result = self.transformer.add_expr([left, right])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "ADD_EXPR"
        assert result.get_lhs() == left
        assert result.get_rhs() == right
    
    def test_add_expr_single_element(self):
        """Test add expression with single element"""
        single = Node("NUM", "5")
        result = self.transformer.add_expr([single])
        
        # Should return the single element
        assert result == single
    
    def test_function_call_transformation(self):
        """Test function call transformation"""
        func_name = Node("ID", "test_func")
        arg1 = Node("NUM", "1")
        arg2 = Node("NUM", "2")
        
        result = self.transformer.function_call([func_name, arg1, arg2])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "FUNCTION_CALL"
        assert result.get_lhs() == func_name
        assert result.get_rhs() == [arg1, arg2]
    
    def test_function_call_no_args(self):
        """Test function call with no arguments"""
        func_name = Node("ID", "test_func")
        result = self.transformer.function_call([func_name])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "FUNCTION_CALL"
        assert result.get_lhs() == func_name
        assert result.get_rhs() == []
    
    def test_return_stmt_with_value(self):
        """Test return statement with value"""
        value = Node("NUM", "42")
        result = self.transformer.return_stmt([value])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "RETURN"
        assert result.get_lhs() == value
    
    def test_return_stmt_empty(self):
        """Test empty return statement"""
        result = self.transformer.return_stmt([])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "RETURN"
        assert result.get_lhs() is None
    
    def test_param_list_transformation(self):
        """Test parameter list transformation"""
        param1 = Node("ID", "x")
        param2 = Node("ID", "y")
        result = self.transformer.param_list([param1, param2])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "PARAM_LIST"
        assert result.get_lhs() == [param1, param2]
    
    def test_factor_transformation(self):
        """Test factor transformation"""
        inner_node = Node("NUM", "42")
        result = self.transformer.factor([inner_node])
        
        assert isinstance(result, Node)
        assert result.get_kind() == "FACTOR"
        assert result.get_lhs() == inner_node