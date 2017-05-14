import sys
import os

from gensim import models
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/db")
from table_wikitext_nodes import Table_nodes

model = models.Doc2Vec.load('wikitext_doc2vec.model')

#keys = model.docvecs.doctags.keys()
keys = ["Final Fantasy VIII", "Final Fantasy X", "Dragon Ball"]
for key in keys:
	print(key)
	np_array = np.array(model.docvecs[key])
	np_str = ",".join(str(i) for i in np_array)
	node = Table_nodes(title=key, vector=np_str)
	node.insert()