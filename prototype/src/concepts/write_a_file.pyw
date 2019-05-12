import os
import logging
from datetime import datetime

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,os.pardir,'files')
log_file = os.path.join(out_path, 'write_a_file.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG,format='%(levelname)s - %(asctime)s - %(message)s')
try:
    logging.info("STARTED - {}:  ... Logger configured".format(__file__))

    out_file = os.path.join(out_path,'test.txt')
    logging.info("Attempting to write file {}".format(out_file))
    with open(out_file,'a+') as f:
        f.write('File Updated at: {}\n'.format(datetime.now()))
    logging.info("COMPLETED - {}".format(__file__))
    #raise Exception("Test Exception")
except Exception as e:
    logging.exception("FAILED - {}  with {}".format(__file__,e))
