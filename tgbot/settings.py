import sys
from loguru import logger

# Logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("logs/file_1.log", rotation="500 MB")
