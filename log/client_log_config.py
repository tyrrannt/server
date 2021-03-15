import logging

logger = logging.getLogger("client")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
fh = logging.FileHandler("client.log", encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

logger = logging.getLogger('client')
