
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

if __name__ == "__main__":
	log = Log.getLogger()
	print("start")
	#print(str(log.__dict__))
	#log.appender.file.File="../../var/log/log"
	#print(str(log.getAllApependers))
	log.debug("this is debug")
	log.info("this is info")
	#log.warning("this is warning")
	log.error("this is error")
	#log.exception("this is exception")


