import logging
from os import getenv, environ
from typing import Tuple
from colorama import Fore, Style


class FormatadorColorido(logging.Formatter):
    """
    Formatter personalizado que adiciona cores ANSI às mensagens de log baseadas no nível de severidade.

    Herda de logging.Formatter e utiliza a biblioteca colorama para colorização.
    """

    FORMATO = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

    MAPA_DE_CORES = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def __init__(self):
        """Inicializa o formatador com o formato padrão definido na classe."""
        super().__init__(self.FORMATO)

    def format(self, record: logging.LogRecord) -> str:
        """
        Formata o registro de log, aplicando cor à mensagem.

        Este método modifica temporariamente o atributo `msg` do registro para incluir
        códigos de cor ANSI e, em seguida, restaura a mensagem original para evitar
        efeitos colaterais em outros handlers que possam usar o mesmo registro.

        Args:
            record (logging.LogRecord): O objeto contendo os dados do evento de log.

        Returns:
            str: A string de log formatada e colorida.
        """
        cor = self.MAPA_DE_CORES.get(record.levelno, Fore.WHITE)

        # Guardamos a mensagem original para não modificar o record permanentemente
        # Isso é crucial se houver múltiplos handlers (ex: um para arquivo e outro para console)
        msg_original = record.msg
        record.msg = f"{cor}{msg_original}{Style.RESET_ALL}"

        resultado_formatado = super().format(record)

        # Restauramos a mensagem original caso o 'record' seja reutilizado
        record.msg = msg_original

        return resultado_formatado


def _get_env_logger_data() -> Tuple[str, str]:
    """
    Recupera e valida as configurações de log das variáveis de ambiente.

    Busca por 'LOGGER_NAME' e 'LOGGING_LEVEL'. Se não encontrados ou inválidos,
    aplica valores padrão ('default_utils' e 'INFO') e ajusta o ambiente.

    Returns:
        Tuple[str, str]: Uma tupla contendo (nome_do_logger, nivel_do_log).
    """
    nome_logger = getenv("LOGGER_NAME")
    if nome_logger is None:
        print("Aviso: LOGGER_NAME não reconhecido, fixando em 'default_utils'")
        nome_logger = "default_utils"
        environ["LOGGER_NAME"] = nome_logger  # Define para processos futuros

    nivel_log_str = getenv("LOGGING_LEVEL", "INFO").upper()
    niveis_validos = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    if nivel_log_str not in niveis_validos:
        print(f"Aviso: Nível de LOG '{nivel_log_str}' não reconhecido, fixando em 'INFO'")
        nivel_log_str = "INFO"

    return nome_logger, nivel_log_str


def create_logger() -> logging.Logger:
    """
    Configura e retorna uma instância de Logger pronta para uso.

    O logger é configurado com um StreamHandler (saída padrão) utilizando o
    FormatadorColorido. Implementa um padrão singleton básico verificando se
    o logger já possui handlers para evitar duplicação de logs.

    Returns:
        logging.Logger: Instância do logger configurado.
    """
    nome_logger, nivel_log_str = _get_env_logger_data()
    logger = logging.getLogger(nome_logger)

    # Evitar handlers duplicados (Idempotência)
    # Se o logger já tiver handlers, assumimos que já foi configurado e o retornamos.
    if logger.handlers:
        return logger

    nivel_log = getattr(logging, nivel_log_str, logging.INFO)
    logger.setLevel(nivel_log)

    # Configuração do handler de console
    manipulador = logging.StreamHandler()
    manipulador.setFormatter(FormatadorColorido())
    logger.addHandler(manipulador)

    # Impede que o log propague para o logger root (evita duplicidade se o root tiver config)
    logger.propagate = False

    return logger


def recreate_logger() -> logging.Logger:
    """
    Recria e reconfigura o logger global, forçando a re-leitura das variáveis de ambiente.

    Remove os handlers anteriores do logger antigo (se houver) para evitar duplicação ou vazamento,
    configura o novo logger de acordo com as novas variáveis do ambiente e atualiza a referência
    global `log` no módulo.

    Returns:
        logging.Logger: Instância do logger configurado e atualizado.
    """
    global log

    # Limpa handlers do logger antigo antes de mudar a referência
    if "log" in globals() and log:
        for handler in list(log.handlers):
            log.removeHandler(handler)

    nome_logger, nivel_log_str = _get_env_logger_data()
    logger = logging.getLogger(nome_logger)

    # Limpa handlers pré-existentes no novo logger (se houver) para evitar duplicados
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    nivel_log = getattr(logging, nivel_log_str, logging.INFO)
    logger.setLevel(nivel_log)

    # Configuração do handler de console
    manipulador = logging.StreamHandler()
    manipulador.setFormatter(FormatadorColorido())
    logger.addHandler(manipulador)

    # Impede que o log propague para o logger root (evita duplicidade se o root tiver config)
    logger.propagate = False

    log = logger
    return logger


log = create_logger()