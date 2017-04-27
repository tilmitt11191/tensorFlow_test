
# -*- coding: utf-8 -*-

import sys,os

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_tf_parameters(Base):
	__tablename__ = 'tf_parameters'

	id = Column("id", INTEGER, primary_key=True)
	result = Column("result", INTEGER)
	v0 = Column("v0", FLOAT)
	v1 = Column("v1", FLOAT)
	v2 = Column("v2", FLOAT)
	v3 = Column("v3", FLOAT)
	v4 = Column("v4", FLOAT)
	v5 = Column("v5", FLOAT)
	v6 = Column("v6", FLOAT)
	v7 = Column("v7", FLOAT)
	v8 = Column("v8", FLOAT)
	v9 = Column("v9", FLOAT)

	def __init__(self, id="", result=result, v0=0, v1=0, v2=0, v3=0, v4=0, v5=0, v6=0, v7=0, v8=0, v9=0):
	
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		
		import mysql_operator
		self.db = mysql_operator.Mysql_operator()
		
		self.id = id
		self.result = result
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.v4 = v4
		self.v5 = v5
		self.v6 = v6
		self.v7 = v7
		self.v8 = v8
		self.v9 = v9

	def __repr__(self):
		return 'Table_citations'

	def insert(self):
		if self.id == "":
			self.id = self.db.get_available_id(__class__)
		self.db.insert(self)
		self.db.session.expunge(self)
		self.db.session.close()

	def renewal_insert(self):
		pass

	def close(self):
		self.db.close()
	
	def get_vars(self):
		import inspect
		methods = []
		for method in inspect.getmembers(self, inspect.ismethod):
			methods.append(method[0])
		
		vars = ""
		for var in self.__dir__():
			if var != "db" and var != "metadata" and var !="log" and not var.startswith("_") and not var in methods:
				vars += var + "[" + str(eval("self."+var)) + "]"
		return vars

