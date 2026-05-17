import logging
import os
from pathlib import Path

# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

# Автоматическое создание папки
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logger(module_name: str) -> logging.Logger:
    """Создает изолированный файловый логгер с уровнем DEBUG."""
    logger = logging.getLogger(module_name)

    # ВАЖНО: Принудительно выставляем DEBUG для логгера
    logger.setLevel(logging.DEBUG)

    # Изолируем логгер от глобального root-логгера Python
    logger.propagate = False

    if not logger.handlers:
        log_file_path = LOG_DIR / f"{module_name}.log"

        # Создаем обработчик файлов
        file_handler = logging.FileHandler(
            log_file_path, mode="w", encoding="utf-8"
        )

        # ВАЖНО: Принудительно выставляем DEBUG для обработчика
        file_handler.setLevel(logging.DEBUG)

        # Настраиваем формат
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)

        # Подключаем обработчик
        logger.addHandler(file_handler)

    return logger
