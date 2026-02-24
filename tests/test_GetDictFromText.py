import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from globaltirh_utils.GetDictFromText import get_dict_from_text


class TestGetDictFromText(unittest.TestCase):

    def test_get_dict_from_text_sucesso(self):
        """Teste de sucesso extraindo JSON."""
        texto = 'Texto antes ```json {"chave": "valor"} ``` Texto depois'
        resultado = get_dict_from_text(texto)
        self.assertEqual(resultado, {"chave": "valor"})

    def test_get_dict_from_text_erro_logico(self):
        """Teste com string válida que não contém JSON."""
        texto = "Texto sem json algum"
        with self.assertRaises(ValueError):
            get_dict_from_text(texto)

    def test_get_dict_from_text_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            get_dict_from_text(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)
