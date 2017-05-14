
# -*- coding: utf-8 -*-

import sys,os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/db")
from wikitext_mysql_operator import Mysql_operator
from table_wikitext_nodes import Table_nodes
from table_wikitext_edges import Table_edges

log = Log.getLogger()

log.info("get_edges_by_subtractions.py start.")

db = Mysql_operator()
records = db.session.query(Table_nodes).all()

ids = []
vectors = []
for record in records:
    ids.append(record.id)
    vectors.append(np.array(record.vector.split(","),dtype=float))

log.debug("ids.size[" + str(len(ids)) + "]")
log.debug("vectors.size[" + str(len(vectors)) + "]")

## calc distances between start_node and end_node
for start_id in range(len(ids)):
    for end_id in range(len(ids)):
        if start_id == end_id:
            continue
        if start_id > end_id: #already registerd
            continue
        log.debug("create edge from start[" + str(ids[start_id]) + "] to end[" + str(ids[end_id]) + "]")
        log.debug("start_vec: " + str(vectors[start_id]))
        log.debug("end_vec: " + str(vectors[end_id]))
        log.debug("calc distance")
        distance = float(np.linalg.norm(vectors[start_id] - vectors[end_id]))
        log.debug("distance: " + str(distance))
        edge = Table_edges(start=ids[start_id], end=ids[end_id], relevancy=distance)
        edge.insert()
