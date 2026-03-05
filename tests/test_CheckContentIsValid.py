import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from globaltirh_utils.CheckContentIsValid import check_content_is_valid


class TestCheckContentIsValid(unittest.TestCase):

    def test_check_content_is_valid_sucesso(self):
        """Teste de sucesso com conteúdo válido."""
        content = [
            {"role": "user", "parts": [{"text": "Olá"}]},
            {"role": "model", "parts": [{"text": "Oi"}]},
        ]
        self.assertIsNone(check_content_is_valid(content))

    def test_check_content_is_valid_erro_logico(self):
        """Teste com tipos corretos mas estrutura inválida (erro de lógica/valor)."""
        # 'role' inválido
        content = [{"role": "invalid_role", "parts": [{"text": "Olá"}]}]
        with self.assertRaises(ValueError):
            check_content_is_valid(content)

    def test_check_content_is_valid_tipo_errado(self):
        """Teste com tipo de argumento errado."""
        # Passando um dicionário em vez de uma lista
        with self.assertRaises(TypeError):
            check_content_is_valid({"role": "user", "parts": []})


if __name__ == "__main__":
    unittest.main(verbosity=2)
