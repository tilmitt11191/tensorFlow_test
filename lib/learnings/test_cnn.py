# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

sys.path.append(os.path.dirname(
	os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log
log = Log.getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
#from enwiki_nodes import Table_nodes
from enwiki_nodes import Table_nodes
from enwiki_operator import Mysql_operator

import tensorflow as tf
from tensorflow.contrib.slim.python.slim.nets.inception_v3 import inception_v3_base
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


def parse_sequence_example(serialized, image_feature, caption_feature):
	"""Parses a tensorflow.SequenceExample into an image and caption.

	Args:
	  serialized: A scalar string Tensor; a single serialized SequenceExample.
	  image_feature: Name of SequenceExample context feature containing image
		data.
	  caption_feature: Name of SequenceExample feature list containing integer
		captions.

	Returns:
	  encoded_image: A scalar string Tensor containing a JPEG encoded image.
	  caption: A 1-D uint64 Tensor with dynamically specified length.
	"""
	print("image_feature: " + str(image_feature))
	print("caption_feature: " + str(caption_feature))
	context, sequence = tf.parse_single_sequence_example(
		serialized,
		context_features={
			image_feature: tf.FixedLenFeature([], dtype=tf.string)
		},
		sequence_features={
			caption_feature: tf.FixedLenSequenceFeature([], dtype=tf.int64),
		})

	encoded_image = context[image_feature]
	caption = sequence[caption_feature]
	return encoded_image, caption


def main(argv=None):
	print("this is main")
	log = Log.getLogger()
	db = Mysql_operator()
	#records = db.session.query(Table_nodes).all()
	#records = db.session.query(Table_nodes).filter(Table_nodes.id < 10).all()
	#print(len(records))
	ids = []
	titles = []
	docs = []
	sentences = []
	#for record in records:
	#	ids.append(record.id)
	#	titles.append(record.title)
	#	docs.append(record.doc2vec)
	#	sentences.append(record.sentence)

	#parse_sequence_example(docs[0], sentences[0], ids[0])
	for i in range(10):
		#print(i)
		a = str(i)
		def _print(a,b):
			print(a,b)
			return a
		tmp = _print
		print(tmp)


if __name__ == '__main__':
	tf.app.run()
