
# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l

log = l.getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from table_tf_parameters import Table_tf_parameters
from table_edges import Table_edges

log.info("get_edges_by_subtractions.py start.")

db = mysql_operator.Mysql_operator()
tfps = db.session.query(Table_tf_parameters).all()

import numpy as np
ids = []
vectors = []
for tfp in tfps:
    ids.append(tfp.id)
    vectors.append(np.array([tfp.v0, tfp.v1, tfp.v2, tfp.v3, tfp.v4, tfp.v5, tfp.v6, tfp.v7, tfp.v8, tfp.v9]))

log.debug("ids.size[" + str(len(ids)) + "]")
log.debug("vectors.size[" + str(len(vectors)) + "]")

## calc distances between start_node and end_node
for start_id in range(500, 1000):
#for start_id in range(len(ids)):
    for end_id in range(500, 1000):
    #for end_id in range(len(ids)):
        if start_id == end_id:
            continue
        if start_id > end_id: #already registerd
            continue
        log.debug("create edge from start[" + str(start_id) + "] to end[" + str(end_id) + "]")
        log.debug("start_vec: " + str(vectors[start_id]) + ", end_vec: " + str(vectors[end_id]))
        distance = float(np.linalg.norm(vectors[start_id] - vectors[end_id]))
        log.debug("distance: " + str(distance))
        edge = Table_edges(start=start_id, end=end_id, relevancy=distance)
        edge.insert()
