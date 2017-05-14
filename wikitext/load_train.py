from gensim.models import word2vec, KeyedVectors

model = word2vec.Word2Vec.load("wiki.train.bin")

while True:
	print("input: ")
	word = input()
	result = model.most_similar(word, topn = 5)
	print(result)
