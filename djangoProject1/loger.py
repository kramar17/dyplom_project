import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('main.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

user_logger = logging.getLogger('user_logger')
user_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('user.log', encoding='utf-8')
file_handler.setFormatter(formatter)
user_logger.addHandler(file_handler)

shop_logger = logging.getLogger('user_logger')
shop_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('user.log', encoding='utf-8')
file_handler.setFormatter(formatter)
shop_logger.addHandler(file_handler)