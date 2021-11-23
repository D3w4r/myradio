import os
import logging.config

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(format='%(asctime)s : %(lineno)d - %(message)s', level=logging.INFO, filename=os.getcwd() + '/logs.log', filemode='w')
logger = logging.getLogger(__name__)
