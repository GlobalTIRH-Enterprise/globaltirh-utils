from bs4 import BeautifulSoup
from markdown import markdown

def clean_html_and_markdown(text: str) -> str:
    """
    Limpa uma string de elementos HTML e Markdown.

    Args:
        text (str): A string a ser limpa.

    Returns:
        str: O texto limpo.
    """
    # Remove HTML
    soup = BeautifulSoup(text, "html.parser")
    text_sem_html = soup.get_text()

    # Remove Markdown
    # A conversão de Markdown para texto plano pode ser feita convertendo para HTML e depois extraindo o texto
    html_from_markdown = markdown(text_sem_html)
    soup_from_markdown = BeautifulSoup(html_from_markdown, "html.parser")
    texto_limpo = soup_from_markdown.get_text()

    return texto_limpo