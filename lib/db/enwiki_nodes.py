
# -*- coding: utf-8 -*-
import sys
import os
import inspect

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT, TEXT, LONGTEXT, DATETIME
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/db")
from enwiki_operator import Mysql_operator

Base = declarative_base()
class Table_nodes(Base):
	__tablename__ = 'nodes'

	id = Column("id", INTEGER, primary_key=True)
	title = Column("title", TEXT)
	sentence = Column("sentence", LONGTEXT)
	doc2vec = Column("doc2vec", TEXT)
	tensorflow = Column("tensorflow", TEXT)
	attribute = Column("attribute", TINYTEXT)
	cluster = Column("cluster", TINYTEXT)
	label = Column("label", TINYTEXT)
	image = Column("image", TEXT)
	color = Column("color", TINYTEXT)
	timestamp = Column("timestamp", DATETIME)


	def __init__(self, id="", title="", sentence="", doc2vec="", tensorflow="", attribute="", cluster="", label="", image = "", color="", timestamp=None):
		self.log = Log.getLogger()

		self.db = Mysql_operator()
		
		self.id = id
		self.title = title
		self.sentence = sentence
		self.doc2vec = doc2vec
		self.tensorflow = tensorflow
		self.attribute = attribute
		self.cluster = cluster
		self.label = label
		self.image = image
		self.color = color
		self.timestamp = timestamp

	def __repr__(self):
		return 'Table_nodes'

	def insert(self):
		if self.id == "":
			self.id = self.db.get_available_id(__class__)
		vars_to_encode = ["title", "sentence"]
		for var in vars_to_encode:
			if eval("self." + var) is not None:
				exec("self." + var + " = self." + var + ".encode('utf-8', 'replace')")
		self.db.insert(self)
		for var in vars_to_encode:
			if eval("self." + var) is not None:
				exec("self." + var + " = self." + var + ".decode('utf-8', 'replace')")
		self.db.session.expunge(self)
		self.db.session.close()
		self.db.close()

	def get_id(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")		
		
		##when the records which have same title exist,
		##the id is smallest one of records.
		records = self.db.session.query(__class__).filter(__class__.title==self.title.encode('utf-8')).all()
		if len(records) == 0: #new record
			return self._get_available_id()
			
		id = records[0].id
		for record in records:
			if id > record.id:
				id = record.id
		return id

	def _get_available_id(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		previous_id = 0
		for q in self.db.session.query(__class__).order_by(__class__.id):
			if q.id - previous_id >= 2:
				self.log.debug("id[" + str(q.id) + "] - previous_id[" + str(previous_id) + "] > 2. return " + str(previous_id + 1))
				return previous_id + 1
			previous_id = q.id
		self.log.debug("for loop ended. return " + str(previous_id + 1))
		return previous_id + 1

		
	def get_vars(self):
		methods = []
		for method in inspect.getmembers(self, inspect.ismethod):
			methods.append(method[0])
		
		vars = ""
		for var in self.__dir__():
			if var != "db" and var != "metadata" and var !="log" and not var.startswith("_") and not var in methods:
				vars += var + "[" + str(eval("self."+var)) + "]"
		return vars
