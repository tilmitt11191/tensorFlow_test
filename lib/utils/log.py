# -*- coding: utf-8 -*-
import sys
import os
import logging
from pyspark import SparkContext
from conf import Conf

class Log:

	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		return cls.getSparkLogger(logfile=logfile, conffile=conffile)

	@classmethod
	def getSparkLogger(cls, logfile="", conffile=""):
		
		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		
		#sc = SparkContext.getOrCreate()
		#log4j = sc._jvm.org.apache.log4j
		#logger = log4j.LogManager.getLogger("myLogger")
		#logger = log4j.LogManager.getLogger(__name__)
		#logger = log4j.LogManager.getRootLogger()
		#logger.appender.FILE.File="../../var/log/log"
		#logger.setLevel(log4jLogger.Level.DEBUG)
		#logger.info("aaaa")
		#return logger

		if not 'LOG_DIRS' in os.environ:
			sys.stderr.write('Missing LOG_DIRS environment variable, pyspark logging disabled')
			return 

		file = os.environ['LOG_DIRS'].split(',')[0] + '/log'
		logging.basicConfig(filename=file, level=logging.INFO, 
				format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
		logger = logging.getLogger()
		return logger


