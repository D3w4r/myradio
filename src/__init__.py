import logging.config

logging.basicConfig(format='DateTime : %(asctime)s : Line No. : %(lineno)d - %(message)s', level=logging.INFO, filename='logs.log', filemode='w')
logger = logging.getLogger(__name__)
