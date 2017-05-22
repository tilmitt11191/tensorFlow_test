# -*- coding: utf-8 -*-

import sys,os
import numpy as np
from pyspark import SparkContext
#import multiprocessing
#from multiprocessing import Pool

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/db")
from wikitext_mysql_operator import Mysql_operator
from table_wikitext_nodes import Table_nodes
from table_wikitext_edges import Table_edges

log = Log.getLogger()

def calc_edge_between(param):

	start_id = param[0]
	end_id = param[1]
	vectors = param[2]
	if start_id == end_id:
		return True
	elif start_id > end_id: #already registerd
		return True

	m = "from[" + str(start_id) + "] to[" + str(end_id) + "]"
	print(m)
	log.debug(m)

	#log.debug("create edge from start[" + str(start_id) + "] to end[" + 
		#str(end_id) + "]")
	#log.debug("start_vec: " + str(vectors[start_id]))
	#log.debug("end_vec: " + str(vectors[end_id]))
	#log.debug("calc distance")
	distance = float(np.linalg.norm(vectors[start_id] - vectors[end_id]))
	#print("distance[" + str(distance) + "]")
	#log.debug("distance: " + str(distance))
	edge = Table_edges(start=start_id, end=end_id, relevancy=distance)
	edge.insert()
	return True

if __name__ == "__main__":
	log.info("get_edges_by_subtractions.py start.")

	#sc = SparkContext()
	sc = SparkContext.getOrCreate()
	db = Mysql_operator()
	records = db.session.query(Table_nodes).all()

	ids = []
	doc2vec = {}

	for record in records:
		ids.append(record.id)
		doc2vec[record.id] = np.array(record.doc2vec.split(","),dtype=float)

	log.debug("ids.size[" + str(len(ids)) + "]")
	log.debug("vectors.size[" + str(len(doc2vec)) + "]")

	for start_id in [ids[0], ids[1]]:
		log.debug("start_id[" + str(start_id) + "] create param")
		params = sc.parallelize([[start_id, end_id, doc2vec] for end_id in ids])
		log.debug("params.map")
		result = params.map(calc_edge_between)

	log.debug("Finished!!")
	print("Finished!!")

"""
Spark Master at spark://ubuntuVM:7077
URL: spark://ubuntuVM:7077
REST URL: spark://ubuntuVM:6066 (cluster mode)
Alive Workers: 0
Cores in use: 0 Total, 0 Used
Memory in use: 0.0 B Total, 0.0 B Used
Applications: 0 Running, 0 Completed
Drivers: 0 Running, 0 Completed
Status: ALIVE
"""
#-executor-memory
