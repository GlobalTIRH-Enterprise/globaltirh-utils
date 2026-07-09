import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from utils_global.gcp.storage.ValidarGsutilLink import validar_gsutil_link

class TestValidarGsutilLink(unittest.TestCase):

    def test_validar_gsutil_link_sucesso(self):
        """Teste de sucesso."""
        link = "gs://bucket/folder/uuid/file.pdf"
        # 4 partes após gs://: bucket, folder, uuid, file.pdf
        # Função espera 4 partes por padrão
        self.assertIsNone(validar_gsutil_link(link))

    def test_validar_gsutil_link_erro_logico(self):
        """Teste com link fora do padrão (número de partes incorreto)."""
        link = "gs://bucket/file.pdf"  # Só 2 partes
        with self.assertRaises(ValueError):
            validar_gsutil_link(link)

    def test_validar_gsutil_link_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            validar_gsutil_link(123)

if __name__ == "__main__":
    unittest.main(verbosity=2)