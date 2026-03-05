import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_global.StringToBool import string_to_bool

class TestStringToBool(unittest.TestCase):

    def test_string_to_bool_sucesso(self):
        """Teste de sucesso convertendo strings válidas."""
        self.assertTrue(string_to_bool("true"))
        self.assertTrue(string_to_bool("verdadeiro"))
        self.assertFalse(string_to_bool("FALSE"))
        self.assertFalse(string_to_bool("0"))

    def test_string_to_bool_erro_logico(self):
        """Teste com string válida mas que não é booleana."""
        with self.assertRaises(ValueError):
            string_to_bool("talvez")

    def test_string_to_bool_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            string_to_bool(123)

if __name__ == "__main__":
    unittest.main(verbosity=2)
