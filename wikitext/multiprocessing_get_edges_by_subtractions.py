
# -*- coding: utf-8 -*-

import sys,os
import numpy as np
import multiprocessing
from multiprocessing import Pool

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

	num_of_core = multiprocessing.cpu_count()
	p = Pool(num_of_core * 8 - 1)

	db = Mysql_operator()
	records = db.session.query(Table_nodes).all()

	ids = []
	vectors = {}

	for record in records:
		ids.append(record.id)
		vectors[record.id] = np.array(record.vector.split(","),dtype=float)

	log.debug("ids.size[" + str(len(ids)) + "]")
	log.debug("vectors.size[" + str(len(vectors)) + "]")
	#for x, y in [[start, end] for start in ids for end in ids]:
	#	print("x: " + str(x) + ", y: " + str(y))
	for start_id in ids:
		params = [[start_id, end_id, vectors] for end_id in ids]
		result = p.map(calc_edge_between, params)

	log.debug("Finished!!")
	print("Finished!!")
	"""
	result = p.map(
		calc_edge_between,
		[[start, end] for start, end in zip(ids, ids)]
		)
	"""
	"""
	list = []
	for start_id in range(len(ids)):
		for end_id in range(len(ids)):
			if start_id == end_id:
				continue
			if start_id > end_id: #already registerd
				continue
			list.append([start_id, end_id])

	print(len(list))
	"""
	"""
	## calc distances between start_node and end_node
	for start_id in range(len(ids)):
		for end_id in range(len(ids)):
			if start_id == end_id:
				continue
			if start_id > end_id: #already registerd
				continue
			print("from[" + str(ids[start_id]) + "] to[" + str(ids[end_id]) + "]")
			log.debug("create edge from start[" + str(ids[start_id]) + "] to end[" + str(ids[end_id]) + "]")
			log.debug("start_vec: " + str(vectors[start_id]))
			log.debug("end_vec: " + str(vectors[end_id]))
			log.debug("calc distance")
			distance = float(np.linalg.norm(vectors[start_id] - vectors[end_id]))
			print("distance[" + str(distance) + "]")
			log.debug("distance: " + str(distance))
			edge = Table_edges(start=ids[start_id], end=ids[end_id], relevancy=distance)
			edge.insert()
	"""
