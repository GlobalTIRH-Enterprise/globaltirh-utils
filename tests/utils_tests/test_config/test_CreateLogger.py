import unittest
import sys
import os
import logging
import importlib
import io
from unittest.mock import MagicMock, patch

# Adiciona o diretório raiz ao path para importar o pacote helpers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import helpers.config.CreateLogger as cl_module

class TestCreateLogger(unittest.TestCase):

    def setUp(self):
        # Salva o estado original do ambiente
        self.orig_env = {
            "LOGGER_NAME": os.environ.get("LOGGER_NAME"),
            "LOGGING_LEVEL": os.environ.get("LOGGING_LEVEL"),
            "K_SERVICE": os.environ.get("K_SERVICE"),
            "K_REVISION": os.environ.get("K_REVISION")
        }
        # Garante que as variáveis de Cloud Run estejam limpas por padrão
        os.environ.pop("K_SERVICE", None)
        os.environ.pop("K_REVISION", None)

    def tearDown(self):
        # Restaura o estado original do ambiente
        for key, val in self.orig_env.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val

        # Recarrega o módulo para deixar o estado limpo para os próximos testes
        importlib.reload(cl_module)

    def test_recreate_logger(self):
        # Garante carregamento limpo para o teste padrão local
        importlib.reload(cl_module)
        original_log = cl_module.log

        # Verifica o logger inicial padrão
        self.assertIsNotNone(original_log)
        self.assertEqual(original_log.name, "default_utils")

        # Modifica as variáveis de ambiente
        os.environ["LOGGER_NAME"] = "my_custom_logger"
        os.environ["LOGGING_LEVEL"] = "DEBUG"

        # Chama recreate_logger
        new_log = cl_module.recreate_logger()

        # Verifica se o novo logger foi criado com as novas configurações
        self.assertEqual(new_log.name, "my_custom_logger")
        self.assertEqual(new_log.level, logging.DEBUG)

        # Verifica se a referência global no módulo foi atualizada
        self.assertIs(cl_module.log, new_log)

        # Verifica se os handlers do logger anterior foram removidos
        self.assertEqual(len(original_log.handlers), 0)

        # Verifica se o novo logger tem exatamente 1 handler
        self.assertEqual(len(new_log.handlers), 1)

    def test_create_logger_cloud_run(self):
        # Configura as variáveis de ambiente do Cloud Run
        os.environ["K_SERVICE"] = "test-service"
        os.environ["K_REVISION"] = "test-revision"

        # Mock de google.cloud.logging
        mock_google = MagicMock()
        mock_gcp_logging = mock_google.cloud.logging

        # Patch sys.stdout para capturar prints e o módulo google.cloud.logging
        with patch.dict("sys.modules", {
            "google": mock_google,
            "google.cloud": mock_google.cloud,
            "google.cloud.logging": mock_gcp_logging
        }), patch("sys.stdout", new=io.StringIO()) as mock_stdout:

            importlib.reload(cl_module)

            # Verifica se o print de detecção foi emitido
            stdout_output = mock_stdout.getvalue()
            sys.__stdout__.write(f"\nDEBUG STDOUT: {stdout_output}\n")

            self.assertIn("Ambiente Cloud Run detectado", stdout_output)
            self.assertIn("Configurando google-cloud-logging", stdout_output)

            # Verifica se o client setup_logging foi chamado
            mock_gcp_logging.Client.assert_called_once()
            mock_gcp_logging.Client().setup_logging.assert_called_once()

            # Verifica se o logger retornado propaga logs (para GCP)
            self.assertTrue(cl_module.log.propagate)

    def test_recreate_logger_cloud_run_ignored(self):
        # Configura as variáveis de ambiente do Cloud Run
        os.environ["K_SERVICE"] = "test-service"
        os.environ["K_REVISION"] = "test-revision"

        # Mock de google.cloud.logging
        mock_google = MagicMock()
        mock_gcp_logging = mock_google.cloud.logging

        with patch.dict("sys.modules", {
            "google": mock_google,
            "google.cloud": mock_google.cloud,
            "google.cloud.logging": mock_gcp_logging
        }), patch("sys.stdout", new=io.StringIO()) as mock_stdout:

            importlib.reload(cl_module)

            # Agora, limpa o buffer do stdout e chama recreate_logger
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

            current_log = cl_module.log
            recreated_log = cl_module.recreate_logger()

            # Verifica que o logger não foi recriado (é o mesmo objeto de log)
            self.assertIs(current_log, recreated_log)

            # Verifica se o aviso de que recreate foi ignorado foi printado no stdout
            stdout_output = mock_stdout.getvalue()
            sys.__stdout__.write(f"\nDEBUG STDOUT RECREATE: {stdout_output}\n")
            
            self.assertIn("Tentativa de recriar o logger no ambiente Cloud Run foi ignorada", stdout_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
