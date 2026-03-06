import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_global.GuessMimeType import guess_mimetype


class TestGuessMimeType(unittest.TestCase):

    def test_guess_mimetype_sucesso(self):
        """Teste de sucesso com extensão conhecida."""
        with self.subTest(file="documento.pdf"):
            self.assertEqual(guess_mimetype("documento.pdf"), "application/pdf")

        with self.subTest(file="dados.csv", expected="text/csv"):
            self.assertEqual(guess_mimetype("dados.csv"), "text/csv")  # mimetypes ou fallback

    def test_guess_mimetype_erro_logico(self):
        """
        Teste com string válida mas extensão desconhecida (retorna None).
        Isso não levanta exceção, mas é o comportamento de falha lógica de detecção.
        """
        self.assertIsNone(guess_mimetype("arquivo.xyz_desconhecido"))

    def test_guess_mimetype_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            guess_mimetype(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)