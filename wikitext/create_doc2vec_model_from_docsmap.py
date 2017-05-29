# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re
import time

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import models
from gensim.models.doc2vec import LabeledSentence

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/documents")
from wiki import Wiki

class LabeledLineSentence(object):
	def __init__(self, filename):
		self.filename = filename
	def __iter(self):
		for uid, line in enumerate(open(filename)):
			yield LabeledSentence(words = line.split(), labels = ['sent_%s' % uid])


start_time = time.perf_counter()
sentences = []
#docs = ["./enwiki-articles1-sample"]
docs = ["../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302"]
#docs = [
#	"../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302",
#	"../../data/wikitext/datasets/enwiki-20170501-pages-articles2.xml-p30304p88444"
#	]
wiki = Wiki()
docs_map = wiki.convert_docs_to_map(docs, doc_type="enwiki")
for title,contents in docs_map.items():
	sentences.append(LabeledSentence(words=contents, tags=[title]))
wiki.substitute_redirect_articles(docs_map)
wiki.delete_redirect_only_articles(docs_map)
print("create sentences finished. sentences len is " + str(len(sentences)))
print("perf_counter = {:.7f}".format(time.perf_counter() - start_time))

print("create model")
start_time = time.perf_counter()
#model = models.Doc2Vec(
#	sentences, dm=0, size=300, window=15, alpha=.025,
#	min_alpha=.025, min_count=1, sample=1e-6)
model = models.Doc2Vec(dm=0, size=300, window=15, alpha = .025, min_alpha =.025, min_count = 1)
model.build_vocab(sentences)
print("perf_counter = {:.7f}".format(time.perf_counter() - start_time))

print('\ntrain start')
for epoch in range(20):
	print('Epoch: {}'.format(epoch + 1))
	start_time = time.perf_counter()
	model.train(sentences,  total_examples=len(sentences), epochs=model.iter)
	model.alpha -= (0.025 - 0.0001) / 19
	model.min_alpha = model.alpha
	print("perf_counter = {:.7f}".format(time.perf_counter() - start_time))
	
print("save model")
model.save('wikitext_articles1_doc2vec.model')