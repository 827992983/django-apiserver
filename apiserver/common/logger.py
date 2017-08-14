import logging
from constants import APISERVER_LOG_FILE

g_log_init = False

def __log_init():
    global g_log_init
    if not g_log_init:
        logging.basicConfig(level=logging.DEBUG,  
                    filename=APISERVER_LOG_FILE,  
                    filemode='a',  
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        g_log_init = True

def log_info(logstr):
    __log_init()
    logging.info(logstr)

def log_debug(logstr):
    __log_init()
    logging.debug(logstr)

def log_error(logstr):
    __log_init()
    logging.error(logstr)