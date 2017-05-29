# -*- coding: utf-8 -*-
"""conver documents format to map and doc2vec LabeledSentence."""
import os
import sys
import re
import codecs
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log

class Wiki:
	"""class Wiki."""

	def __init__(self):
		"""init."""
		self.log = Log.getLogger()
		# rule of removing xml tags from docs
		self.p = re.compile(r"<[^>]*?>|\[\[|\]\]|{{[^>]*?}}|\n", flags=re.MULTILINE)
		#self.p = re.compile(r"<[^>]*?>|\[\[|\]\]|{{[^>]*?}}|\n", flags=re.DOTALL)
		self.log.debug("class " + __class__.__name__ + " created.")

	def convert_docs_to_map(self, docs, doc_type="enwiki"):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		if not isinstance(docs, list):
			sys.exit(
				"docs not list at" +
				__class__.__name__ + "." + sys._getframe().f_code.co_name
				)

		docs_map = {}

		for doc in docs:
			if doc_type == "enwiki":
				self.analyze_enwiki_docs(doc, docs_map)
			else:
				sys.exit(
					doc_type + " is invalid at " +
					__class__.__name__ + "." + sys._getframe().f_code.co_name
					)
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return docs_map. size: " + str(len(docs_map)))
		return docs_map

	def substitute_redirect_articles(self, docs_map):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		for title,contents in docs_map.items():
			if re.match("redirect title=", contents):
				redirect_title=contents.lstrip("redirect title=")
				self.log.debug("title[ " + title + "] this is redirect to :" + redirect_title)
				if redirect_title in docs_map:
					self.log.debug("has key")
					docs_map[title] = docs_map[redirect_title]
				else:
					self.log.debug("not have key")
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	def analyze_enwiki_docs(self, doc, docs_map):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		root = ET.parse(doc).getroot()
		pages = [el for el in list(root) if re.match(".*page$", el.tag)]
		self.log.debug("num of pages: " + str(len(pages)))

		times = 1
		num = len(pages)
		for page in pages:
			self.log.debug("times[" + str(times) + "] num[" + str(num) + "]")
			title, contents = self.get_title_and_contents_of_enwiki_doc(page)
			self.log.debug("title: " + title)
			#print("contents: " + contents)
			docs_map[title] = contents
			times += 1

		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	def get_title_and_contents_of_enwiki_doc(self, page):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		title = ""
		contents = ""
		if page is None:
			print("page is none")
			return "", ""
		for el in list(page):
			if re.match(".*redirect$", el.tag):
				contents = "redirect title=" + el.attrib["title"]
			if re.match(".*title$", el.tag):
				title = el.text
			if re.match(".*revision$", el.tag) and contents is "":
				contents = self.get_contents_of_enwiki_doc(el)
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return title, contents

	def get_titles_and_first_sentences_of_enwiki_doc(self, docs_map):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		sentences = {}
		for title, contents in docs_map.items():
			array = contents.split(".")
			if len(array) > 0:
				sentence = array[0]
			else:
				sentence = ""
			sentences[title] = sentence
		return sentences

	def get_contents_of_enwiki_doc(self, revision):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		for el in revision:
			if re.match(".*text$", el.tag):
				return self.p.sub("", el.text)
		self.log.warning("revision not have text")
		return ""

	def delete_redirect_only_articles(self, docs_map):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		# for k, v in docs_map.items():
			# if re.match("redirect title=", v):
				# del(docs_map[k])
		for k in list(docs_map):
			if re.match("redirect title=", docs_map[k]):
				del(docs_map[k])
		# new_docs_map = {}
		# new_docs_map = dict((k, v) for k, v in docs_map.items() if not re.match("redirect title=", v))
		# return new_docs_map
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
