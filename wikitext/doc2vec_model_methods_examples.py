import sys
import os
from gensim import models
from gensim.models.doc2vec import LabeledSentence
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.decomposition import TruncatedSVD
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/documents")
from wiki import Wiki

model = models.Doc2Vec.load('wikitext_doc2vec.model')

# print(dir(model))
"""
['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__ignoreds', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__numpys', '__recursive_saveloads', '__reduce__', '__reduce_ex__', '__repr__', '__scipys', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_adapt_by_suffix', '_do_train_job', '_load_specials', '_minimize_model', '_raw_word_count', '_save_specials', '_smart_save', 'accuracy', 'alpha', 'batch_words', 'build_vocab', 'cbow_mean', 'clear_sims', 'comment', 'corpus_count', 'create_binary_tree', 'cum_table', 'dbow', 'dbow_words', 'delete_temporary_training_data', 'dm', 'dm_concat', 'dm_tag_count', 'docvecs', 'doesnt_match', 'estimate_memory', 'evaluate_word_pairs', 'finalize_vocab', 'hashfxn', 'hs', 'infer_vector', 'init_sims', 'initialize_word_vectors', 'intersect_word2vec_format', 'iter', 'layer1_size', 'load', 'load_word2vec_format', 'log_accuracy', 'log_evaluate_word_pairs', 'make_cum_table', 'max_vocab_size', 'min_alpha', 'min_alpha_yet_reached', 'min_count', 'model_trimmed_post_training', 'most_similar', 'most_similar_cosmul', 'n_similarity', 'negative', 'null_word', 'predict_output_word', 'random', 'raw_vocab', 'reset_from', 'reset_weights', 'sample', 'save', 'save_word2vec_format', 'scale_vocab', 'scan_vocab', 'score', 'seed', 'seeded_vector', 'sg', 'similar_by_vector', 'similar_by_word', 'similarity', 'sort_vocab', 'sorted_vocab', 'syn0_lockf', 'syn1neg', 'total_train_time', 'train', 'train_count', 'update_weights', 'vector_size', 'window', 'wmdistance', 'workers', 'wv']
"""
# print(str(len(model.docvecs.doctags)))
# 29200

# print(str(len(model.raw_vocab)))
# 0

# print(str(dir(model.docvecs)))
"""
['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__ignoreds', '__init__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__numpys', '__recursive_saveloads', '__reduce__', '__reduce_ex__', '__repr__', '__scipys', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_adapt_by_suffix', '_int_index', '_key_index', '_load_specials', '_save_specials', '_smart_save', 'borrow_from', 'clear_sims', 'count', 'doctag_syn0', 'doctag_syn0_lockf', 'doctag_syn0norm', 'doctags', 'doesnt_match', 'estimated_lookup_memory', 'index_to_doctag', 'indexed_doctags', 'init_sims', 'load', 'mapfile_path', 'max_rawint', 'most_similar', 'n_similarity', 'note_doctag', 'offset2doctag', 'reset_weights', 'save', 'similarity', 'similarity_unseen_docs', 'trained_item']

"""
#print(str(dir(model.docvecs.doctags)))
"""
['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
"""

#print(dir(model.finalize_vocab))
"""
['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__func__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
"""

#text = "\n".join(str(x) for x in model.docvecs.doctags.keys())
#print(text)

# shows the similar words
# print(model.most_similar('suppli'))
# => KeyError: "word 'suppli' not in vocabulary"
#result = model.docvecs.most_similar('Bomber Mafia', topn = 5)
#text = "\n".join(str(x) for x in result)
#print(text)

# shows the learnt embedding
#print(model['Bomber Mafia'])

# shows the similar docs with id = 2
#result = model.docvecs.most_similar(str(2))
#text = "\n".join(str(x) for x in result)
#print(text)

#print(len(model.docvecs.offset2doctag))
# => 29200


#sentences = []
#docs = ["./enwiki-articles1-sample"]
#docs = ["../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302"]
#docs = [
#	"../../data/wikitext/datasets/enwiki-20170501-pages-articles1.xml-p10p30302",
#	"../../data/wikitext/datasets/enwiki-20170501-pages-articles2.xml-p30304p88444"
#	]
#wiki = Wiki()
#docs_map = wiki.convert_docs_to_map(docs, doc_type="enwiki")
#for title,contents in docs_map.items():
#	sentences.append(LabeledSentence(words=contents, tags=[title]))
#wiki.substitute_redirect_articles(docs_map)
#wiki.delete_redirect_only_articles(docs_map)
#print("#################")
#print(sentences[1].words)
#print("#################")
#print(sentences[2].words)
#print("#################")
#print(sentences[3].words)
#print("#################")

#f = open("bomber.txt", "r")
#pred_vec = model.infer_vector(f.readlines())
#actual_tags = map(lambda x: unmark_tag(x), sentences[docid].tags)
#pred_tags = model.docvecs.most_similar([pred_vec], topn=5)
#print(pred_tags)