

import tensorflow as tf

with tf.Session() as sess:
	#tf.device("/cpu:0")

	hello = sess.run(tf.constant('hello, tensorflow!'))

	print(hello)