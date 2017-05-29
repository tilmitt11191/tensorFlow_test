
# -*- coding: utf-8 -*-

import unittest
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from enwiki_nodes import Table_nodes as Enwiki_nodes

class MySQL_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.log = l().getLogger()
		cls.db = mysql_operator.Mysql_operator()
		cls.log.info("\n\nMySQL_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		pass
		#import sqlalchemy
		#self.engine = sqlalchemy.create_engine("mysql+pymysql://alladmin:admin@localhost/paper_graph?charset=utf8", echo=False)
		#from sqlalchemy.orm import sessionmaker
		#Session = sessionmaker(bind=self.engine)
		#self.db.session = Session()
	"""
	def test_tf_insert(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		from table_tf_parameters import Table_tf_parameters as tfp
		tfp = tfp()
		print(tfp.get_vars())
		tfp.insert()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	def test_insert_invalid_string(self):
		node = Enwiki_nodes(
			title = "Delta (letter)",
			sentence = "'''Delta''' (uppercase '''Δ''', lowercase '''δ''' or '''𝛿'''; {{lang|el|Δέλτα}} ''Délta''; Modern Greek {{IPA-el|ˈðelta|}}&lt;ref&gt;&lt;/ref&gt;) is the fourth letter of the [[Greek alphabet]]"
			)
		node.insert()


if __name__ == '__main__':
	unittest.main()


