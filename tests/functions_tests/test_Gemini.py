import unittest
from unittest.mock import MagicMock, patch, mock_open

from functions.cloud.gemini import (
    call_gemini,
    call_gemini_streaming,
)


class TestGeminiNonStreaming(unittest.TestCase):
    """Testes para a função síncrona (sem streaming)."""

    @patch("functions.cloud.gemini.CallGemini.Client")
    @patch("functions.cloud.gemini.CallGemini.types")
    def test_non_streaming_simple_text(self, mock_types, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "Resposta Gemini"
        mock_client.models.generate_content.return_value = mock_response

        resp = call_gemini(
            prompt="Olá",
            project="proj",
            location="us-central1",
            model_name="gemini-pro"
        )

        self.assertEqual(resp, "Resposta Gemini")
        mock_client.models.generate_content.assert_called_once()

    @patch("functions.cloud.gemini.CallGemini.Client")
    @patch("functions.cloud.gemini.CallGemini.guess_mimetype")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dados_arquivo")
    @patch("functions.cloud.gemini.CallGemini.types")
    def test_non_streaming_with_local_file(self, mock_types, mock_file, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "application/pdf"
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "Analise PDF"
        mock_client.models.generate_content.return_value = mock_response

        call_gemini(
            prompt="Analise",
            project="proj",
            location="loc",
            model_name="model",
            arquivos=["documento.pdf"]
        )

        mock_types.Part.from_bytes.assert_called_with(
            data=b"dados_arquivo", mime_type="application/pdf"
        )

    @patch("functions.cloud.gemini.CallGemini.Client")
    @patch("functions.cloud.gemini.CallGemini.guess_mimetype")
    @patch("functions.cloud.gemini.CallGemini.types")
    def test_non_streaming_with_gcs_file(self, mock_types, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "image/png"
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "Resposta"
        mock_client.models.generate_content.return_value = mock_response

        call_gemini(
            prompt="Veja imagem",
            project="proj",
            location="loc",
            model_name="model",
            arquivos="gs://bucket/imagem.png"
        )

        mock_types.Part.from_uri.assert_called_with(
            file_uri="gs://bucket/imagem.png", mime_type="image/png"
        )


class TestGeminiStreaming(unittest.TestCase):
    """Testes para a função com streaming."""

    @patch("functions.cloud.gemini.CallGeminiStreaming.Client")
    def test_streaming_simple_text(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        chunk1 = MagicMock()
        chunk1.text = "Parte 1"
        chunk2 = MagicMock()
        chunk2.text = "Parte 2"
        mock_client.models.generate_content_stream.return_value = [chunk1, chunk2]

        resp = call_gemini_streaming(
            prompt="Stream",
            project="proj",
            location="loc",
            model_name="model",
            return_only_text=True
        )

        self.assertEqual(resp, "Parte 1Parte 2")
        mock_client.models.generate_content_stream.assert_called_once()

    @patch("functions.cloud.gemini.CallGeminiStreaming.Client")
    @patch("functions.cloud.gemini.CallGeminiStreaming.guess_mimetype")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dados_arquivo")
    @patch("functions.cloud.gemini.CallGeminiStreaming.types")
    def test_streaming_with_local_file(self, mock_types, mock_file, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "application/pdf"
        mock_client = mock_client_cls.return_value
        mock_client.models.generate_content_stream.return_value = []

        call_gemini_streaming(
            prompt="Analise",
            project="proj",
            location="loc",
            model_name="model",
            arquivos=["documento.pdf"]
        )

        mock_types.Part.from_bytes.assert_called_with(
            data=b"dados_arquivo", mime_type="application/pdf"
        )

    @patch("functions.cloud.gemini.CallGeminiStreaming.Client")
    @patch("functions.cloud.gemini.CallGeminiStreaming.guess_mimetype")
    @patch("functions.cloud.gemini.CallGeminiStreaming.types")
    def test_streaming_with_gcs_file(self, mock_types, mock_guess_mime, mock_client_cls):
        mock_guess_mime.return_value = "image/png"
        mock_client = mock_client_cls.return_value
        mock_client.models.generate_content_stream.return_value = []

        call_gemini_streaming(
            prompt="Veja imagem",
            project="proj",
            location="loc",
            model_name="model",
            arquivos="gs://bucket/imagem.png"
        )

        mock_types.Part.from_uri.assert_called_with(
            file_uri="gs://bucket/imagem.png", mime_type="image/png"
        )


if __name__ == "__main__":
    unittest.main()