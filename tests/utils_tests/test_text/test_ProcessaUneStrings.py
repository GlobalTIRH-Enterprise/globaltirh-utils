import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from helpers.text.ProcessaUneStrings import processa_une_strings

class TestProcessaUneStrings(unittest.TestCase):

    def test_processa_une_strings_sucesso(self):
        """Teste de sucesso removendo duplicatas e unindo."""
        lista = [
            "  Olá  ",
            "mundo",
            "olá",
            "MUNDO",
        ]  # "olá" normalizado == "olá", "MUNDO" == "mundo"
        # Esperado: "  Olá  " (primeiro) "mundo" (primeiro). "olá" é duplicado de "  Olá  ".
        self.assertEqual(processa_une_strings(lista), "  Olá   mundo")

    def test_processa_une_strings_erro_logico(self):
        """
        Teste com lista vazia (caso de borda).
        """
        self.assertEqual(processa_une_strings([]), "")

    def test_processa_une_strings_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            processa_une_strings("não é uma lista")

if __name__ == "__main__":
    unittest.main(verbosity=2)