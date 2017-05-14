from gensim.models import word2vec
"""
model = word2vec.Word2Vec(
"../../data/wikitext/wikitext-103-raw/wiki.train.raw")
print(model.wv.vocab["i"])
for vocab in model.wv.vocab:
	print(model.wv.vocab[vocab])
#result = model.most_similar("role", topn = 5)
"""

sentences = word2vec.Text8Corpus("../../data/wikitext/wikitext-103-raw/wiki.train.raw")
model = word2vec.Word2Vec(sentences, workers=28, min_count=5)
model.save("wiki.train.bin")
result = model.most_similar("game", topn = 5)
print(result)
