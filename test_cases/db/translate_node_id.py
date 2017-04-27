# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l

log = l.getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from table_tf_parameters import Table_tf_parameters

db = mysql_operator.Mysql_operator()
tfps = db.session.query(Table_tf_parameters).all()

offset = 14999

for tfp in tfps:
    print(tfp.id + offset)
    new_tfp = Table_tf_parameters(\
        id = tfp.id + offset, \
        result=tfp.result,\
		v0=tfp.v0,\
		v1=tfp.v1,\
		v2=tfp.v2,\
		v3=tfp.v3,\
		v4=tfp.v4,\
		v5=tfp.v5,\
		v6=tfp.v6,\
		v7=tfp.v7,\
		v8=tfp.v8,\
		v9=tfp.v9)
    new_tfp.insert()
    