import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_global.VerificaTipo import deco_verifica_tipo

class TestVerificaTipo(unittest.TestCase):

    def test_deco_verifica_tipo_sucesso(self):
        """Teste se a função decorada funciona normalmente com tipos corretos."""

        @deco_verifica_tipo
        def func_teste(a: int) -> int:
            return a + 1

        self.assertEqual(func_teste(1), 2)

    def test_deco_verifica_tipo_erro_logico(self):
        """
        O decorator não lança erro lógico, ele lança TypeError se os tipos não baterem.
        Aqui vamos testar se ele ignora anotação 'Any'.
        """
        from typing import Any

        @deco_verifica_tipo
        def func_teste(a: Any):
            return a

        # Não deve levantar erro
        self.assertEqual(func_teste(1), 1)
        self.assertEqual(func_teste("a"), "a")

    def test_deco_verifica_tipo_tipo_errado(self):
        """Teste se a função decorada lança TypeError com input errado."""

        @deco_verifica_tipo
        def func_teste(a: int):
            return a

        with self.assertRaises(TypeError):
            func_teste("não é int")

if __name__ == "__main__":
    unittest.main(verbosity=2)
