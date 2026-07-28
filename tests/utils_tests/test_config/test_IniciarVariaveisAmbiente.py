import unittest
from unittest.mock import patch
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from helpers.config.IniciarVariaveisAmbiente import inicializar_variaveis_de_ambiente


class TestIniciarVariaveisAmbiente(unittest.TestCase):

    # @patch("globaltirh_utils.IniciarVariaveisAmbiente.load_dotenv")
    # @patch("globaltirh_utils.IniciarVariaveisAmbiente.os.path.exists")
    # def test_inicializar_variaveis_de_ambiente_sucesso(self, mock_exists, mock_load_dotenv):
    #     """Teste de sucesso encontrando arquivo .env."""
    #     mock_exists.return_value = True
    #     mock_load_dotenv.return_value = True

    #     # Simula encontrar na primeira tentativa
    #     resultado = inicializar_variaveis_de_ambiente()
    #     self.assertTrue(resultado)

    def test_init_variaveis_env_erro_logico(self):
        """Teste falhando ao não encontrar nenhum arquivo e sem variável de ambiente de fallback."""
        # False significa que não conseguiu carregar nada
        os.environ.pop("envs_text", None)
        resultado = inicializar_variaveis_de_ambiente(possible_locations=[""])
        self.assertFalse(resultado)

    # def test_init_variaveis_env_tipo_errado(self):
    #     """Teste com tipo errado para 'possible_locations'."""
    #     with self.assertRaises(TypeError):
    #         inicializar_variaveis_de_ambiente(possible_locations="não é uma lista")


if __name__ == "__main__":
    unittest.main(verbosity=2)