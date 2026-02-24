import unittest
from datetime import datetime, timezone
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from globaltirh_utils.TempoToBrasilia import tempo_to_brasilia

class TestTempoToBrasilia(unittest.TestCase):

    def test_tempo_to_brasilia_sucesso(self):
        """Teste de sucesso convertendo datetime UTC."""
        dt_utc = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt_br = tempo_to_brasilia(dt_utc)
        # Brasilia é UTC-3
        self.assertEqual(dt_br.hour, 9)
        self.assertEqual(str(dt_br.tzinfo), "America/Sao_Paulo")

    def test_tempo_to_brasilia_erro_logico(self):
        """
        Teste com float 'infinito' - tipo correto (float) mas valor inválido para conversão.
        Isso deve causar OverflowError ou ValueError dependendo da plataforma.
        """
        ts_invalido = float("inf")
        with self.assertRaises((OverflowError, ValueError, OSError)):
            tempo_to_brasilia(ts_invalido)

    def test_tempo_to_brasilia_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            tempo_to_brasilia("não é data nem float")

if __name__ == "__main__":
    unittest.main(verbosity=2)
