import logging.config

logging.basicConfig(format='%(asctime)s : %(lineno)d - %(message)s', level=logging.INFO, filename='src/logs.log', filemode='w')
logger = logging.getLogger(__name__)
