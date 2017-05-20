# -*- coding: utf-8 -*-
import sys
import logging
import logging.handlers
from pyspark import SparkContext
from conf import Conf

class Log:

	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		exec_env = Conf.getconf("exec_env")
		if exec_env == "normal":
			return cls.getNormalLogger(logfile=logfile, conffile=conffile)
		elif exec_env == "spark":
			return cls.getNormalLogger(logfile=logfile, conffile=conffile)
		else:
			sys.exit("getLogger Type Error[" + str(exec_env) + "]")

	@classmethod
	def getNormalLogger(cls, logfile="", conffile=""):

		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		loglevel = Conf.getconf("loglevel", conffile=conffile)
		rotate_log_size = Conf.getconf("rotate_log_size")

		logger = logging.getLogger()
		
		if len(logger.handlers) < 1:
			#fh = logging.FileHandler(filename="../../var/log/log2")
			#logger.addHandler(fh)
			rfh = logging.handlers.RotatingFileHandler(
				filename=logfile,
				maxBytes=rotate_log_size, 
				backupCount=Conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			logger.addHandler(rfh)

		#logging.basicConfig(filename="../../var/log/log2")

		id_ = id(logger)
		logger.setLevel(eval("logging."+loglevel))
		logger.debug("return logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
		return logger


	@classmethod
	def getSparkLogger(cls, logfile="", conffile=""):
		
		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		sc = SparkContext()
		log4jLogger = sc._jvm.org.apache.log4j
		log4j.appender.FILE.File="../../var/log/log"
		logger = log4jLogger.LogManager.getLogger()

		return logger



