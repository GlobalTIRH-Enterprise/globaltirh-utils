import unittest
import sys
import os
import logging

# Adiciona o diretório raiz ao path para importar o pacote helpers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

class TestCreateLogger(unittest.TestCase):

    def setUp(self):
        # Salva o estado original do ambiente
        self.orig_env = {
            "LOGGER_NAME": os.environ.get("LOGGER_NAME"),
            "LOGGING_LEVEL": os.environ.get("LOGGING_LEVEL")
        }

    def tearDown(self):
        # Restaura o estado original do ambiente
        for key, val in self.orig_env.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val

    def test_recreate_logger(self):
        # Importa de forma limpa o logger e a nova função recreate_logger
        from helpers.config.CreateLogger import log as original_log, recreate_logger
        import helpers.config.CreateLogger as cl_module

        # Verifica o logger inicial padrão
        self.assertIsNotNone(original_log)
        self.assertEqual(original_log.name, "default_utils")

        # Modifica as variáveis de ambiente
        os.environ["LOGGER_NAME"] = "my_custom_logger"
        os.environ["LOGGING_LEVEL"] = "DEBUG"

        # Chama recreate_logger
        new_log = recreate_logger()

        # Verifica se o novo logger foi criado com as novas configurações
        self.assertEqual(new_log.name, "my_custom_logger")
        self.assertEqual(new_log.level, logging.DEBUG)

        # Verifica se a referência global no módulo foi atualizada
        self.assertIs(cl_module.log, new_log)

        # Verifica se os handlers do logger anterior foram removidos
        self.assertEqual(len(original_log.handlers), 0)

        # Verifica se o novo logger tem exatamente 1 handler
        self.assertEqual(len(new_log.handlers), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
