
# -*- coding: utf-8 -*-

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../../tutorials/mnist/MNIST_data/", one_hot=True)

# trainデータの件数
print("mnist.train.num_examples[" + str(mnist.train.num_examples) + "]")
  #=> 55000

# testデータの件数
print("mnist.test.num_examples[" + str(mnist.test.num_examples) +"]")
  #=> 10000

# validationデータの件数
print("mnist.validation.num_examples[" + str(mnist.validation.num_examples) + "]")
  #=> 5000



from matplotlib import pylab as plt
import matplotlib.cm as cm

plt.imshow(mnist.validation.images[0].reshape(28, 28), cmap = cm.Greys_r)
for i in range(mnist.test.num_examples):
#for i in range(3):
	print("i:" + str(i))
	plt.imshow(mnist.validation.images[i].reshape(28, 28), cmap = cm.Greys_r)
	plt.savefig("../../data/mnist/" + str(i) + ".png")
	
