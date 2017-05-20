# -*- coding: utf-8 -*-
import sys
from pyspark import SparkContext
from conf import Conf

class Log:

	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		return cls.getNormalLogger(logfile=logfile, conffile=conffile)

	@classmethod
	def getSparkLogger(cls, logfile="", conffile=""):
		
		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		sc = SparkContext()
		log4jLogger = sc._jvm.org.apache.log4j
		log4j.appender.FILE.File="../../var/log/log"
		logger = log4jLogger.LogManager.getLogger()

		return logger



