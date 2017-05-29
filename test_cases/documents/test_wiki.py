# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/documents")
from wiki import Wiki

class Wiki_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.log = Log.getLogger()
		cls.log.info("\n\nIEEEXplore_test.setUpClass finished.\n---------- start ---------")

	def setUp(self):
		self.wiki = Wiki()

	"""
	def test_convert_docs_to_map(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		docs = []
		#docs.append("../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302")
		docs.append("enwiki-articles1-sample")
		docs_map = self.wiki.convert_docs_to_map(docs, doc_type="enwiki")
		self.assertEqual(docs_map["AccessibleComputing"], "redirect title=Computer accessibility")
	"""
	"""
	def test_substitute_redirect_articles(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		docs = []
		docs.append("enwiki-articles1-sample")
		docs_map = self.wiki.convert_docs_to_map(docs, doc_type="enwiki")
		self.assertEqual(docs_map["Anarchism Redirect Test"], "redirect title=Anarchism")
		self.wiki.substitute_redirect_articles(docs_map)
		self.assertEqual(docs_map["Anarchism Redirect Test"], docs_map["Anarchism"])
	"""
	"""
	def test_delete_redirect_only_articles(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		docs = []
		docs.append("enwiki-articles1-sample")
		docs_map = self.wiki.convert_docs_to_map(docs, doc_type="enwiki")
		self.assertEqual(docs_map["Anarchism Redirect Test"], "redirect title=Anarchism")
		self.wiki.delete_redirect_only_articles(docs_map)
		print("docs_map: " + str(len(docs_map)))
		#self.assertEqual(len(docs_map),2)
	"""
	def test_get_titles_and_first_sentences_of_enwiki_doc(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		docs = []
		#docs.append("../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302")
		docs.append("enwiki-articles1-sample")
		docs_map = self.wiki.convert_docs_to_map(docs, doc_type="enwiki")
		self.assertEqual(docs_map["AccessibleComputing"], "redirect title=Computer accessibility")
		self.wiki.substitute_redirect_articles(docs_map)
		self.wiki.delete_redirect_only_articles(docs_map)
		sentences = self.wiki.get_titles_and_first_sentences_of_enwiki_doc(docs_map)
		print(len(sentences))
		print(sentences["Anarchism"])
		for k,v in sentences.items():
			print("title: " + k)
			print("sentence: " + v)
	
if __name__ == '__main__':
	unittest.main()
