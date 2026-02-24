import unittest
from typing import Optional, Union, List, Any
try:
    from globaltirh_utils.VerificaTipo import deco_verifica_tipo, verifica_tipo
except ImportError:
    # Fallback to allow running directly from tests/ folder without package installation
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from globaltirh_utils.VerificaTipo import deco_verifica_tipo, verifica_tipo

class TestDecoVerificaTipo(unittest.TestCase):

    def test_basic_types_success(self):
        @deco_verifica_tipo
        def soma(a: int, b: int) -> int:
            return a + b
        
        self.assertEqual(soma(1, 2), 3)
        self.assertEqual(soma(a=10, b=20), 30)

    def test_basic_types_failure(self):
        @deco_verifica_tipo
        def soma(a: int, b: int) -> int:
            return a + b
            
        with self.assertRaises(TypeError) as cm:
            soma("1", 2)
        self.assertIn("Parâmetro 'a' deveria ser do tipo 'int'", str(cm.exception))

    def test_union_types_success(self):
        @deco_verifica_tipo
        def process_id(id: Union[int, str]):
            return str(id)

        self.assertEqual(process_id(123), "123")
        self.assertEqual(process_id("abc"), "abc")

    def test_union_types_failure(self):
        @deco_verifica_tipo
        def process_id(id: Union[int, str]):
            return str(id)

        with self.assertRaises(TypeError) as cm:
            process_id(1.5)
        self.assertIn("Parâmetro 'id' deveria ser do tipo", str(cm.exception))

    def test_optional_types(self):
        @deco_verifica_tipo
        def greet(name: Optional[str] = None):
            if name:
                return f"Hello, {name}"
            return "Hello, stranger"

        self.assertEqual(greet("Alice"), "Hello, Alice")
        self.assertEqual(greet(None), "Hello, stranger")
        self.assertEqual(greet(), "Hello, stranger")
        
        with self.assertRaises(TypeError):
            greet(123)

    def test_list_generic_types(self):
        # Note: Validating deep structures like List[int] is complex. 
        # The current implementation likely only checks against the base class 'list'
        # or fails open if it can't validate deep types.
        # Let's verify behavior for List.
        
        @deco_verifica_tipo
        def process_items(items: List[str]):
            return len(items)

        self.assertEqual(process_items(["a", "b"]), 2)
        
        # Depending on implementation details, this might accept any list if deep check isn't implemented
        # But it should definitely reject non-lists
        with self.assertRaises(TypeError):
            process_items("not a list")

    def test_mixed_args_kwargs(self):
        @deco_verifica_tipo
        def config(host: str, port: int, debug: bool = False):
            return f"{host}:{port} (debug={debug})"

        self.assertEqual(config("localhost", 8080), "localhost:8080 (debug=False)")
        self.assertEqual(config(port=9090, host="127.0.0.1", debug=True), "127.0.0.1:9090 (debug=True)")

        with self.assertRaises(TypeError):
            config("localhost", "8080") # port should be int

class TestLegacyVerificaTipo(unittest.TestCase):
    def test_legacy_direct_call(self):
        # Should pass without error
        verifica_tipo([(1, int, "id"), ("test", str, "name")])
        
        # Should raise error
        with self.assertRaises(TypeError) as cm:
            verifica_tipo([(1, str, "id")])
        self.assertIn("Parâmetro 'id' deveria ser do tipo 'str'", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
