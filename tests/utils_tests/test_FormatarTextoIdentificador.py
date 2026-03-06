import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_global.FormatarTextoIdentificador import formatar_texto_para_identificador


class TestFormatarTextoIdentificador(unittest.TestCase):

    def test_formatar_texto_para_identificador_sucesso(self):
        """Teste de sucesso na formatação."""
        texto = "Olá Mundo! Teste de Acentuação, e Pontuação."
        esperado = "ola_mundo!_teste_de_acentuacao_e_pontuacao"
        # A função remove , ; . / \
        # Mas mantem ! ? etc?
        # Revisitando o código: remove r"[,;.\\/]"
        # Então ! permanece? O código diz "Pontuações específicas".
        # O código não remove '!', então 'mundo!' ficaria 'mundo!'.
        # Vamos verificar o comportamento da regex no código lido.
        # pontuacao_remover = r"[,;.\\/]" -> remove , ; . \ /
        # Então manterá !
        # Espaços viram _
        self.assertEqual(
            formatar_texto_para_identificador(texto), "ola_mundo!_teste_de_acentuacao_e_pontuacao"
        )

    def test_formatar_texto_para_identificador_erro_logico(self):
        """
        Teste conceitual de erro lógico/valor.
        Como a função retorna string formatada, 'erro' seria uma string vazia ou inesperada
        dada uma entrada válida, mas aqui testamos consistência.
        Neste caso, vamos testar uma string que resulta em vazio, se isso for considerado erro,
        ou simplesmente garantir que funciona para casos extremos.
        """
        # Se passar apenas pontuação removível, deve retornar string vazia
        self.assertEqual(formatar_texto_para_identificador("..."), "")

    def test_formatar_texto_para_identificador_tipo_errado(self):
        """Teste com tipo errado."""
        with self.assertRaises(TypeError):
            formatar_texto_para_identificador(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)