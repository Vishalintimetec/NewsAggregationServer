import logging
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, name="app", log_dir=None):
        self.name = name
        if log_dir is None:
            current_file = Path(__file__)
            server_dir = current_file.parent.parent
            self.log_dir = server_dir / "log"
        else:
            self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self._setup_handlers()
    def _setup_handlers(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{today}.logs"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    def debug(self, message):
        self.logger.debug(message)
    def info(self, message):
        self.logger.info(message)
    def warning(self, message):
        self.logger.warning(message)
    def error(self, message):
        self.logger.error(message)
    def critical(self, message):
        self.logger.critical(message)
    def exception(self, message):
        self.logger.exception(message)
logger = Logger()