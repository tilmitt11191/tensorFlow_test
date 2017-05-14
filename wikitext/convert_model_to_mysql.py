import sys
import os
import time
from gensim import models
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/db")
from table_wikitext_nodes import Table_nodes

model = models.Doc2Vec.load('wikitext_doc2vec.model')
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

keys = model.docvecs.doctags.keys()
times = 1
#keys = ["Final Fantasy VIII", "Final Fantasy X", "Dragon Ball"]
for key in keys:
	print("times[" + str(times) + "]/[" + str(len(keys)) +"] key: " + key)
	np_array = np.array(model.docvecs[key])
	np_str = ",".join(str(i) for i in np_array)
	node = Table_nodes(title=key.encode("utf-8"), vector=np_str, timestamp=timestamp)
	node.insert()
	times += 1