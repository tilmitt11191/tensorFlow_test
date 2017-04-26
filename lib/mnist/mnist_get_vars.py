from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys, os

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l.getLogger()
log.debug("start")

# 重み変数
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

# バイアス変数
def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

# 畳み込み
def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# プーリング
def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def main(_):
	log.debug("main(_) start")
	# データ取得
	mnist = input_data.read_data_sets('./MNIST_data/', one_hot=True)

	# placeholder作成
	with tf.name_scope('input'):
		x = tf.placeholder(tf.float32, [None, 784], name="x")
		y_ = tf.placeholder(tf.float32, [None, 10], name="y_")

	# 畳み込み１層目
	with tf.name_scope('layer_1'):
		W_conv1 = weight_variable([5, 5, 1, 32])
		b_conv1 = bias_variable([32])
		x_image = tf.reshape(x, [-1,28,28,1])
		h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
		h_pool1 = max_pool_2x2(h_conv1)

	# 畳み込み２層目
	with tf.name_scope('layer_2'):
		W_conv2 = weight_variable([5, 5, 32, 64])
		b_conv2 = bias_variable([64])
		h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
		h_pool2 = max_pool_2x2(h_conv2)

	# 全結合層
	with tf.name_scope('full_connect'):
		W_fc1 = weight_variable([7 * 7 * 64, 1024])
		b_fc1 = bias_variable([1024])
		h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
		h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

	# ドロップアウト層
	with tf.name_scope('drop_out'):
		keep_prob = tf.placeholder(tf.float32, name="keep_prob")
		h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

	# 出力層
	with tf.name_scope('output'):
		W_fc2 = weight_variable([1024, 10])
		b_fc2 = bias_variable([10])
		y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

	# optimizer
	with tf.name_scope('optimizer'):
		# 損失関数（交差エントロピー誤差）
		cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
		# 勾配
		train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

	# evaluator
	with tf.name_scope('evaluator'):
		# 精度
		correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

	# セッション
	sess = tf.InteractiveSession()
	sess.run(tf.global_variables_initializer())

	# サマリー
	tf.summary.scalar('cross_entropy', cross_entropy)
	tf.summary.scalar('accuracy', accuracy)

	tf.summary.histogram("weights_conv1", W_conv1)
	tf.summary.histogram("weights_conv2", W_conv2)
	tf.summary.histogram("weights_fc1", W_fc1)
	tf.summary.histogram("weights_fc2", W_fc2)
	tf.summary.histogram("biases_conv1", b_conv1)
	tf.summary.histogram("biases_conv2", b_conv2)
	tf.summary.histogram("biases_fc1", b_fc1)
	tf.summary.histogram("biases_fc2", b_fc2)

	merged = tf.summary.merge_all()
	writer = tf.summary.FileWriter("../../var/log/tensorflow_log", sess.graph)

	# トレーニング
	log.debug("training start")
	for i in range(100):
		log.debug("i[" + str(i) + "]")
		batch = mnist.train.next_batch(50)
		log.debug("got batch")
		
		#if i % 10 == 0:
			# 途中経過
			# train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
			# print("step %d, training accuracy %f" % (i, train_accuracy))
			#summary, loss_val, acc_val = sess.run([merged, cross_entropy, accuracy], feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
			#writer.add_summary(summary, i)
			#print('Step: %d, Loss: %f, Accuracy: %f' % (i, loss_val, acc_val))
		
		# トレーニング実行
		log.debug("run training [" + str(i) + "]")
		train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
		#log.debug(y_conv.eval(feed_dict={ x: batch[0], y_:batch[1], keep_prob: 1.0 })[0])
		#log.debug(np.argmax(y_conv.eval(feed_dict={ x: batch[0], y_:batch[1], keep_prob: 1.0 })[0]))
		

	# 評価
	log.debug("evaluate start")
	print("test accuracy %f" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

if __name__ == '__main__':
	log.debug("__name__: main")
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data', help='Directory for storing input data')
	FLAGS, unparsed = parser.parse_known_args()
	log.debug("tf.app.run start")
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
else:
	log.debug("__name__: else")