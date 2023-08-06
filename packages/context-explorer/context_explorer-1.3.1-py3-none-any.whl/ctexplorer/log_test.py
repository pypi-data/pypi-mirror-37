import logging
import warnings
import sys
import datetime

# Logging
time_str = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
log_filepath = '{}.log'.format(time_str)
logging.captureWarnings(True)
logger = logging.getLogger('py.warnings')
hdlr = logging.FileHandler(log_filepath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
warnings.warn('heyeyeyeyeye')

# Logging to stdout
logger_stdout = logging.getLogger('test')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger_stdout.addHandler(ch)
logger_stdout.setLevel(logging.INFO)
logger_stdout.info('asdfsadfsadf')
