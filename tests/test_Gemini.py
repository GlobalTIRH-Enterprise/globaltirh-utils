import unittest
from unittest.mock import MagicMock, patch, mock_open
from functions_global.cloud.Gemini import call_gemini

class TestGemini(unittest.TestCase):

    @patch("utils_global.functions_global.cloud.Gemini.Client")
    @patch("utils_global.functions_global.cloud.Gemini.types")
    def test_call_gemini_simple_text(self, mock_types, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "Resposta Gemini"
        mock_client.models.generate_content.return_value = mock_response

        resp = call_gemini(
            prompt="Olá",
            project_id="proj",
            location="us-central1",
            model_name="gemini-pro"
        )

        self.assertEqual(resp, "Resposta Gemini")
        mock_client.models.generate_content.assert_called_once()

    @patch("utils_global.functions_global.cloud.Gemini.Client")
    @patch("utils_global.functions_global.cloud.Gemini.guess_mimetype")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dados_arquivo")
    @patch("utils_global.functions_global.cloud.Gemini.types")
    def test_call_gemini_with_local_file(self, mock_types, mock_file, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "application/pdf"
        
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "Analise PDF"
        mock_client.models.generate_content.return_value = mock_response

        call_gemini(
            prompt="Analise",
            project_id="proj",
            location="loc",
            model_name="model",
            arquivos=["documento.pdf"]
        )

        # Verifica se tentou criar a Part a partir dos bytes
        mock_types.Part.from_bytes.assert_called_with(data=b"dados_arquivo", mime_type="application/pdf")

    @patch("utils_global.functions_global.cloud.Gemini.Client")
    @patch("utils_global.functions_global.cloud.Gemini.guess_mimetype")
    @patch("utils_global.functions_global.cloud.Gemini.types")
    def test_call_gemini_with_gcs_file(self, mock_types, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "image/png"
        
        call_gemini(
            prompt="Veja imagem",
            project_id="proj",
            location="loc",
            model_name="model",
            arquivos="gs://bucket/imagem.png"
        )

        # Verifica se tentou criar a Part a partir da URI
        mock_types.Part.from_uri.assert_called_with(file_uri="gs://bucket/imagem.png", mime_type="image/png")

    @patch("utils_global.functions_global.cloud.Gemini.Client")
    def test_call_gemini_stream(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        
        # Mock do iterador de stream
        chunk1 = MagicMock()
        chunk1.text = "Parte 1"
        chunk2 = MagicMock()
        chunk2.text = "Parte 2"
        
        mock_client.models.generate_content_stream.return_value = [chunk1, chunk2]

        resp = call_gemini(
            prompt="Stream",
            project_id="proj",
            location="loc",
            model_name="model",
            stream=True,
            return_only_text=True
        )

        self.assertEqual(resp, "Parte 1Parte 2")
        mock_client.models.generate_content_stream.assert_called_once()

if __name__ == "__main__":
    unittest.main()