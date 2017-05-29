import sys
import os
import time
from gensim import models
import numpy as np
import multiprocessing
from multiprocessing import Pool

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
from enwiki_nodes import Table_nodes
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/documents")
from wiki import Wiki

docs = ["../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302"]
#times = 1

def insert_to_mysql(param):
	title = param[0]
	sentence = param[1]
	vector = param[2]
	max_num = param[3]
	#print("times[" + str(times) + "]/[" + str(max_num) +"], title: " + title)
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	node = Table_nodes(title=title, sentence=sentence, doc2vec=vector, timestamp=timestamp)
	node.insert()
	#times += 1

if __name__ == "__main__":
	model = models.Doc2Vec.load("wikitext_articles1_doc2vec.model")
	keys = model.docvecs.doctags.keys()
	num_of_keys = len(keys)
	print("keys:" + str(num_of_keys))

	wiki = Wiki()
	docs_map = wiki.convert_docs_to_map(docs, doc_type="enwiki")
	wiki.substitute_redirect_articles(docs_map)
	wiki.delete_redirect_only_articles(docs_map)
	sentences = wiki.get_titles_and_first_sentences_of_enwiki_doc(docs_map)
	print("sentences: " + str(len(sentences)))

	num_of_core = multiprocessing.cpu_count()
	#p = Pool(num_of_core * 1 - 1)
	p = Pool(1)
	params = []
	#keys = ["Final Fantasy VIII", "Final Fantasy X", "Dragon Ball"]
	for key in keys:
		sentence = ""
		if key in sentences:
			sentence = sentences[key]
		np_array = np.array(model.docvecs[key])
		np_str = ",".join(str(i) for i in np_array)
		params.append([key, sentence, np_str, num_of_keys])
	print("multiple insert_to_mysql start")
	p.map(insert_to_mysql, params)
	print("Finished!!")
	