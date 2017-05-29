# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log
log = Log.getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
#from enwiki_nodes import Table_nodes
from table_wikitext_nodes import Table_nodes
from enwiki_operator import Mysql_operator

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # or any {'0', '1', '2'}


def main(argv=None):
	print("this is main")
	log = Log.getLogger()
	db = Mysql_operator()
	records = db.session.query(Table_nodes).all()
	print(len(records))



if __name__ == '__main__':
	tf.app.run()