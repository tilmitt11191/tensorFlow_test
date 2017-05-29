import sys
from gensim import models
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.decomposition import TruncatedSVD
from collections import defaultdict

model = models.Doc2Vec.load('wikitext_articles1_doc2vec.model')


def create_sim_vec(model,n_sent):
	print("create_sim_vec start")
	base_name = 'sent_'
	sim_matrix = []
	sim_matrix_apd = sim_matrix.append
	word_matrix = []
	word_matrix_apd = word_matrix.append
	sim_vec = np.zeros(n_sent)
	for i_sent in range(n_sent):
		word_list = []
		word_list_apd = word_list.append
		# sentが存在しない場合があるので、例外処理を入れておく							   
		try:
			for word, sim_val in model.docvecs.most_similar(base_name+str(i_sent)):
				if 'sent_' in word:
					_, s_idx = word.split('_')
					sim_vec[int(s_idx)] = sim_val
				else:
					word_list_apd(word)
		except:
			pass
		sim_matrix_apd(sim_vec)
		word_matrix_apd(word_list)
	print("create_sim_vec finished")
	return sim_matrix, word_matrix

n_sent = len(model.docvecs.doctags)
print("n_sent: " + str(n_sent))
sent_matrix, word_matrix = create_sim_vec(model, n_sent)

def sent_integrate(sim_matrix, n_class):
	print("sent_integrate start")
	whiten(sim_matrix)
	centroid, destortion = kmeans(sim_matrix, n_class, iter = 100, thresh = 1e-05)
	labels, dist = vq(sim_matrix,centroid)
	print("sent_integrate finished")
	return labels

def count_class(labels):
	print("count_class start")
	res_dic = defaultdict(int)
	for label in labels:
		res_dic[label] += 1
	print("count_class finished")
	return res_dic

def count_labeled_data(label_data, labels):
	print("count_labeled_data start")
	result_dict = {}
	for orig_labels, label in zip(label_data, labels):
		labels = np.array(orig_labels.split(), dtype = np.int64)
		if label not in result_dict:
			result_dict[label] = labels
		else:
			result_dict[label] += labels
	print("count_labeled_data finished")
	return result_dict

np.savetxt('sent_matrix',np.array(sent_matrix))
dimention = 300
lsa = TruncatedSVD(dimention)
info_matrix = lsa.fit_transform(sent_matrix)
np.savetxt('info_matrix', np.array(info_matrix))

n_class = 10
labels = sent_integrate(np.array(info_matrix), n_class)
np.savetxt('sent_labels2.csv', labels, delimiter = ',', fmt = '%d')