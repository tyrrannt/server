import logging


logger = logging.getLogger("server")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
fh = logging.FileHandler("server.log", encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

logger = logging.getLogger('server')