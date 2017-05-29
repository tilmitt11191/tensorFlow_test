
"""http://hibari1121.blog.fc2.com/blog-entry-57.html ."""
from gensim import corpora, models
import numpy as np
from numpy import random
random.seed(555)
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.decomposition import TruncatedSVD
from collections import defaultdict
 
article = open('data.txt')
model_basename = './D2V/doc2vec_result/model'
topic_result_basename = './D2V/doc2vec_result/topic'
 
 
articles = []
for x in article:
    articles.append(x)
 
article_list = []
for item in articles:
    itemlist = item.split(' ')
    article_list.append(itemlist)
 
class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
    def __iter(self):
        for uid, line in enumerate(open(filename)):
            yield LabeledSentence(words = line.split(), labels = ['sent_%s' % uid])
 
article_tag = []
count = 0
for item in article_list:
    model = models.doc2vec.LabeledSentence(words = item, tags = ['sent_%s' % count])
    article_tag.append(model)
    count += 1
 
model = models.Doc2Vec(alpha = .025, min_alpha =.025, min_count = 1)
model.build_vocab(article_tag)
 
model.save("my_model.doc2vec")
model_loaded = models.Doc2Vec.load("my_model.doc2vec")
 
for epoch in range(10):
    model.train(article_tag)
    model.alpha -= 0.002
    model.min_alpha = model.alpha
 
def create_sim_vec(model,n_sent):
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
    return sim_matrix, word_matrix
 
n_sent = len(articles)
sent_matrix, word_matrix = create_sim_vec(model, n_sent)
 
def sent_integrate(sim_matrix, n_class):
    whiten(sim_matrix)
    centroid, destortion = kmeans(sim_matrix, n_class, iter = 100, thresh = 1e-05)
    labels, dist = vq(sim_matrix,centroid)
    return labels
 
def count_class(labels):
    res_dic = defaultdict(int)
    for label in labels:
        res_dic[label] += 1
    return res_dic
 
def count_labeled_data(label_data, labels):
    result_dict = {}
    for orig_labels, label in zip(label_data, labels):
        labels = np.array(orig_labels.split(), dtype = np.int64)
        if label not in result_dict:
            result_dict[label] = labels
        else:
            result_dict[label] += labels
    return result_dict
 
np.savetxt('sent_matrix',np.array(sent_matrix))
dimention = 100
lsa = TruncatedSVD(dimention)
info_matrix = lsa.fit_transform(sent_matrix)
np.savetxt('info_matrix', np.array(info_matrix))
 
n_class = 10
labels = sent_integrate(np.array(info_matrix), n_class)
np.savetxt('sent_labels2.csv', labels, delimiter = ',', fmt = '%d')