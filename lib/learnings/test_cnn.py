# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
import codecs

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

class model_sample(object):
	def __init__(self, contents=None):
		self.contents = contents
		self.total_loss = None
		self.global_step = None
		# Reader for the input data.
		self.reader = tf.TFRecordReader()
		#configs
		self.input_file_pattern = "${MSCOCO_DIR}/train-?????-of-00256"
		self.batch_size = 32
		self.values_per_input_shard = 2300
		self.input_queue_capacity_factor = 2
		self.num_input_reader_threads = 1

	def setup_global_step(self):
		"""Sets up the global step Tensor."""
		global_step = tf.Variable(
				initial_value=0,
				name="global_step",
				trainable=False,
				collections=[tf.GraphKeys.GLOBAL_STEP, tf.GraphKeys.GLOBAL_VARIABLES])

		self.global_step = global_step

	def build_inputs(self):
		# Prefetch serialized SequenceExample protos.
		input_queue = prefetch_input_data(
				self.reader,
				self.contents,
				is_training=True,
				batch_size=self.batch_size,
				values_per_shard=self.values_per_input_shard,
				input_queue_capacity_factor=self.input_queue_capacity_factor,
				num_reader_threads=self.num_input_reader_threads)

		# Image processing and random distortion. Split across multiple threads
		# with each thread applying a slightly different distortion.
		assert self.config.num_preprocess_threads % 2 == 0
		images_and_captions = []
		for thread_id in range(self.config.num_preprocess_threads):
			serialized_sequence_example = input_queue.dequeue()
			encoded_image, caption = parse_sequence_example(
					serialized_sequence_example,
					image_feature=self.config.image_feature_name,
					caption_feature=self.config.caption_feature_name)
			image = self.process_image(encoded_image, thread_id=thread_id)
			images_and_captions.append([image, caption])

		# Batch inputs.
		queue_capacity = (2 * self.config.num_preprocess_threads *
			self.config.batch_size)
		images, input_seqs, target_seqs, input_mask = (
				batch_with_dynamic_pad(images_and_captions,
				 batch_size=self.config.batch_size,
				 queue_capacity=queue_capacity))

		self.images = images
		self.input_seqs = input_seqs
		self.target_seqs = target_seqs
		self.input_mask = input_mask


	def build_model(self):
		targets = tf.reshape(self.target_seqs, [-1])
		weights = tf.to_float(tf.reshape(self.input_mask, [-1]))

		# Compute losses.
		losses = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=targets,
						logits=logits)
		batch_loss = tf.div(tf.reduce_sum(tf.multiply(losses, weights)),
				tf.reduce_sum(weights),
				name="batch_loss")
		tf.losses.add_loss(batch_loss)
		total_loss = tf.losses.get_total_loss()

		# Add summaries.
		tf.summary.scalar("losses/batch_loss", batch_loss)
		tf.summary.scalar("losses/total_loss", total_loss)
		for var in tf.trainable_variables():
			tf.summary.histogram("parameters/" + var.op.name, var)

		self.total_loss = total_loss
		self.target_cross_entropy_losses = losses	# Used in evaluation.
		self.target_cross_entropy_loss_weights = weights	# Used in evaluation.

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

def prefetch_input_data(reader,
												contents,
												is_training,
												batch_size,
												values_per_shard,
												input_queue_capacity_factor=16,
												num_reader_threads=1,
												shard_queue_name="filename_queue",
												value_queue_name="input_queue"):
	"""Prefetches string values from disk into an input queue.

	In training the capacity of the queue is important because a larger queue
	means better mixing of training examples between shards. The minimum number of
	values kept in the queue is values_per_shard * input_queue_capacity_factor,
	where input_queue_memory factor should be chosen to trade-off better mixing
	with memory usage.

	Args:
		reader: Instance of tf.ReaderBase.
		file_pattern: Comma-separated list of file patterns (e.g.
				/tmp/train_data-?????-of-00100).
		is_training: Boolean; whether prefetching for training or eval.
		batch_size: Model batch size used to determine queue capacity.
		values_per_shard: Approximate number of values per shard.
		input_queue_capacity_factor: Minimum number of values to keep in the queue
			in multiples of values_per_shard. See comments above.
		num_reader_threads: Number of reader threads to fill the queue.
		shard_queue_name: Name for the shards filename queue.
		value_queue_name: Name for the values input queue.

	Returns:
		A Queue containing prefetched string values.
	"""
	data_files = []
	for pattern in contents:
		data_files.extend(tf.gfile.Glob(pattern))
	if not data_files:
		tf.logging.fatal("Found no input files matching %s", file_pattern)
	else:
		tf.logging.info("Prefetching values from %d files matching %s",
										len(data_files), file_pattern)

	if is_training:
		filename_queue = tf.train.string_input_producer(
				data_files, shuffle=True, capacity=16, name=shard_queue_name)
		min_queue_examples = values_per_shard * input_queue_capacity_factor
		capacity = min_queue_examples + 100 * batch_size
		values_queue = tf.RandomShuffleQueue(
				capacity=capacity,
				min_after_dequeue=min_queue_examples,
				dtypes=[tf.string],
				name="random_" + value_queue_name)
	else:
		filename_queue = tf.train.string_input_producer(
				data_files, shuffle=False, capacity=1, name=shard_queue_name)
		capacity = values_per_shard + 3 * batch_size
		values_queue = tf.FIFOQueue(
				capacity=capacity, dtypes=[tf.string], name="fifo_" + value_queue_name)

	enqueue_ops = []
	for _ in range(num_reader_threads):
		_, value = reader.read(filename_queue)
		enqueue_ops.append(values_queue.enqueue([value]))
	tf.train.queue_runner.add_queue_runner(tf.train.queue_runner.QueueRunner(
			values_queue, enqueue_ops))
	tf.summary.scalar(
			"queue/%s/fraction_of_%d_full" % (values_queue.name, capacity),
			tf.cast(values_queue.size(), tf.float32) * (1. / capacity))

	return values_queue

def batch_with_dynamic_pad(images_and_captions,
													 batch_size,
													 queue_capacity,
													 add_summaries=True):
	"""Batches input images and captions.

	This function splits the caption into an input sequence and a target sequence,
	where the target sequence is the input sequence right-shifted by 1. Input and
	target sequences are batched and padded up to the maximum length of sequences
	in the batch. A mask is created to distinguish real words from padding words.

	Example:
		Actual captions in the batch ('-' denotes padded character):
			[
				[ 1 2 5 4 5 ],
				[ 1 2 3 4 - ],
				[ 1 2 3 - - ],
			]

		input_seqs:
			[
				[ 1 2 3 4 ],
				[ 1 2 3 - ],
				[ 1 2 - - ],
			]

		target_seqs:
			[
				[ 2 3 4 5 ],
				[ 2 3 4 - ],
				[ 2 3 - - ],
			]

		mask:
			[
				[ 1 1 1 1 ],
				[ 1 1 1 0 ],
				[ 1 1 0 0 ],
			]

	Args:
		images_and_captions: A list of pairs [image, caption], where image is a
			Tensor of shape [height, width, channels] and caption is a 1-D Tensor of
			any length. Each pair will be processed and added to the queue in a
			separate thread.
		batch_size: Batch size.
		queue_capacity: Queue capacity.
		add_summaries: If true, add caption length summaries.

	Returns:
		images: A Tensor of shape [batch_size, height, width, channels].
		input_seqs: An int32 Tensor of shape [batch_size, padded_length].
		target_seqs: An int32 Tensor of shape [batch_size, padded_length].
		mask: An int32 0/1 Tensor of shape [batch_size, padded_length].
	"""
	enqueue_list = []
	for image, caption in images_and_captions:
		caption_length = tf.shape(caption)[0]
		input_length = tf.expand_dims(tf.subtract(caption_length, 1), 0)

		input_seq = tf.slice(caption, [0], input_length)
		target_seq = tf.slice(caption, [1], input_length)
		indicator = tf.ones(input_length, dtype=tf.int32)
		enqueue_list.append([image, input_seq, target_seq, indicator])

	images, input_seqs, target_seqs, mask = tf.train.batch_join(
			enqueue_list,
			batch_size=batch_size,
			capacity=queue_capacity,
			dynamic_pad=True,
			name="batch_and_pad")

	if add_summaries:
		lengths = tf.add(tf.reduce_sum(mask, 1), 1)
		tf.summary.scalar("caption_length/batch_min", tf.reduce_min(lengths))
		tf.summary.scalar("caption_length/batch_max", tf.reduce_max(lengths))
		tf.summary.scalar("caption_length/batch_mean", tf.reduce_mean(lengths))

	return images, input_seqs, target_seqs, mask

def main(argv=None):
	print("this is main")
	log = Log.getLogger()
	db = Mysql_operator()
	#records = db.session.query(Table_nodes).all()
	records = db.session.query(Table_nodes).filter(Table_nodes.id < 10).all()
	print(len(records))
	ids = []
	titles = []
	docs = []
	sentences = []
	contents = [(record.doc2vec, record.sentence, 'utf-8') for record in records]
	print(len(contents))
	#for record in records:
	#	ids.append(record.id)
	#	titles.append(record.title)
	#	docs.append(record.doc2vec)
	#	sentences.append(record.sentence)
	
	# Build the TensorFlow graph.
	g = tf.Graph()
	with g.as_default():
		log.debug("graph setup starts")
		model = model_sample(contents=contents)
		model.build_inputs()
		model.build_model()
		model.setup_global_step()
		learning_rate = tf.constant(2.0)
		optimizer = "SGD"
		clip_gradients = 5.0
		initial_learning_rate = 2.0
		learning_rate_decay_factor = 0.5
		num_examples_per_epoch = 19858
		batch_size = 32
		num_epochs_per_decay = 8.0

		learning_rate_decay_fn = None
		learning_rate = tf.constant(initial_learning_rate)
		if learning_rate_decay_factor > 0:
			num_batches_per_epoch = (
				num_examples_per_epoch / batch_size)
			decay_steps = int(
				num_batches_per_epoch * num_epochs_per_decay)
			def _learning_rate_decay_fn(learning_rate, global_step):
				return tf.train.exponential_decay(
					learning_rate,
					global_step,
					decay_steps=decay_steps,
					decay_rate=learning_rate_decay_factor,
					staircase=True)
			learning_rate_decay_fn = _learning_rate_decay_fn
			log.debug("define learning_rate_decay_fn")
		log.debug(str(learning_rate_decay_fn))
		# Set up the training ops.
		train_op = tf.contrib.layers.optimize_loss(
				loss=model.total_loss,
				global_step=model.global_step,
				learning_rate=learning_rate,
				optimizer=optimizer,
				clip_gradients=clip_gradients,
				learning_rate_decay_fn=learning_rate_decay_fn)
	
if __name__ == '__main__':
	tf.app.run()
