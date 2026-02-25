import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json

# Adiciona o diretório raiz ao path para importar o pacote globaltirh_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from globaltirh_utils.SalvarCredenciais import salvar_credenciais


class TestSalvarCredenciais(unittest.TestCase):

    @patch("globaltirh_utils.SalvarCredenciais.log")
    def test_deve_pular_setup_on_server(self, mock_log):
        """Teste se a função retorna cedo quando on_server é True."""
        salvar_credenciais(
            on_server=True,
            usar_google_application_credentials=True,
            temporary_folder="tmp",
            temporary_file="creds.json",
        )
        mock_log.info.assert_called()
        self.assertIn("ON_SERVER=TRUE", mock_log.info.call_args[0][0])

    @patch("globaltirh_utils.SalvarCredenciais.log")
    def test_deve_pular_setup_flag_false(self, mock_log):
        """Teste se a função retorna cedo quando usar_google_application_credentials é False."""
        salvar_credenciais(
            on_server=False,
            usar_google_application_credentials=False,
            temporary_folder="tmp",
            temporary_file="creds.json",
        )
        mock_log.info.assert_called()
        self.assertIn(
            "USAR GOOGLE APPLICATION CREDENTIALS = FALSE", mock_log.info.call_args[0][0]
        )

    @patch("globaltirh_utils.SalvarCredenciais.log")
    def test_deve_pular_setup_ja_definido(self, mock_log):
        """Teste se a função retorna cedo quando GOOGLE_APPLICATION_CREDENTIALS já existe."""
        with patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "/path/exists"}):
            salvar_credenciais(
                on_server=False,
                usar_google_application_credentials=True,
                temporary_folder="tmp",
                temporary_file="creds.json",
            )
            mock_log.info.assert_called()
            self.assertIn("já definida", mock_log.info.call_args[0][0])

    @patch("globaltirh_utils.SalvarCredenciais.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_credenciais_full_json(self, mock_file, mock_path):
        """Teste salvando credenciais a partir de FULL_GCP_CREDENTIAL."""
        creds_json = json.dumps({"project_id": "teste", "private_key": "key"})

        # Mock do Path para retornar um caminho string válido
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = "/tmp/creds.json"

        with patch.dict(os.environ, {"FULL_GCP_CREDENTIAL": creds_json}, clear=True):
            salvar_credenciais(
                on_server=False,
                usar_google_application_credentials=True,
                temporary_folder="tmp",
                temporary_file="creds.json",
            )

            # Verifica se o arquivo foi escrito
            mock_file.assert_called()
            # Verifica se a variável de ambiente foi definida
            self.assertEqual(
                os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"), "/tmp/creds.json"
            )

    @patch("globaltirh_utils.SalvarCredenciais.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_credenciais_individuais(self, mock_file, mock_path):
        """Teste salvando credenciais a partir de variáveis individuais."""
        env_vars = {
            "CREDENCIAL_TYPE": "service_account",
            "CREDENCIAL_PROJECT_ID": "proj",
            "CREDENCIAL_PRIVATE_KEY_ID": "id",
            "CREDENCIAL_PRIVATE_KEY": "---BEGIN\\nKEY---",
            "CREDENCIAL_CLIENT_EMAIL": "email",
            "CREDENCIAL_ID": "client_id",
            "CREDENCIAL_AUTH_URI": "auth",
            "CREDENCIAL_TOKEN_URIN": "token",
            "CREDENCIAL_AUTH_PROVIDER_X509_CERT_URL": "cert_url",
            "CREDENCIAL_CLIENT_X509_CERT_URL": "client_cert",
            "CREDENCIAL_UNIVERSE_DOMAIN": "domain",
        }

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = "/tmp/creds.json"

        with patch.dict(os.environ, env_vars, clear=True):
            salvar_credenciais(
                on_server=False,
                usar_google_application_credentials=True,
                temporary_folder="tmp",
                temporary_file="creds.json",
            )

            mock_file.assert_called()
            self.assertEqual(
                os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"), "/tmp/creds.json"
            )

    def test_erro_falta_variavel(self):
        """Teste se levanta erro quando falta variável obrigatória."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                salvar_credenciais(
                    on_server=False,
                    usar_google_application_credentials=True,
                    temporary_folder="tmp",
                    temporary_file="creds.json",
                )


if __name__ == "__main__":
    unittest.main()