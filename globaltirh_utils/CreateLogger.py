import logging
from typing import cast
from colorama import Fore, Style


class FormatadorColorido(logging.Formatter):
    """
    Formatter personalizado que adiciona cores ANSI às mensagens de log baseadas no nível de severidade.
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
        super().__init__(self.FORMATO)

    def format(self, record: logging.LogRecord) -> str:
        # A forma mais segura: formata a mensagem completamente com os argumentos primeiro.
        resultado_formatado = super().format(record)

        # Pega a cor correspondente ou Branco como padrão
        cor = self.MAPA_DE_CORES.get(record.levelno, Fore.WHITE)

        # Envelopa a linha inteira formatada com as cores ANSI
        return f"{cor}{resultado_formatado}{Style.RESET_ALL}"


class LogGerenciavel(logging.Logger):
    """
    Classe de Logger customizada que permite alterar suas configurações
    em tempo de execução sem perder a referência da memória.
    """

    def set_level(self, logging_level: str) -> None:
        """
        Método 'set' para atualizar o nível de severidade do log dinamicamente.
        """
        nivel_log_str = logging_level.upper()
        niveis_validos = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

        if nivel_log_str not in niveis_validos:
            print(f"Aviso: Nível de LOG '{nivel_log_str}' não reconhecido. Mantendo o atual.")
            return

        novo_nivel = getattr(logging, nivel_log_str)
        self.setLevel(novo_nivel)
        self.info(f"Nível de log atualizado para: {nivel_log_str}")


# Instruímos o módulo logging do Python a usar nossa classe customizada
# sempre que um novo logger for instanciado.
logging.setLoggerClass(LogGerenciavel)


def create_logger(
    logger_name: str = "default_globaltirh_utils", logging_level: str = "INFO"
) -> LogGerenciavel:
    """
    Configura e retorna uma instância do Logger.
    """
    nivel_log_str = logging_level.upper()
    niveis_validos = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    if nivel_log_str not in niveis_validos:
        print(f"Aviso: Nível de LOG '{nivel_log_str}' não reconhecido, fixando em 'INFO'")
        nivel_log_str = "INFO"

    # Usamos cast para evitar alertas falsos de tipagem em IDEs e Linters
    logger = cast(LogGerenciavel, logging.getLogger(logger_name))

    # Idempotência: Se já tem handlers, apenas atualiza o nível e retorna
    if logger.handlers:
        logger.set_level(nivel_log_str)
        return logger

    # Configuração inicial caso o logger esteja sendo criado pela primeira vez
    nivel_log = getattr(logging, nivel_log_str, logging.INFO)
    logger.setLevel(nivel_log)

    manipulador = logging.StreamHandler()
    manipulador.setFormatter(FormatadorColorido())
    logger.addHandler(manipulador)
    logger.propagate = False

    return logger


# Instância global disponível para importação
log = create_logger()
