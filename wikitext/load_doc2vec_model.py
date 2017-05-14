import sys
from gensim import models

model = models.Doc2Vec.load('wikitext_doc2vec.model')
# create_binary_tree
#print(str(model.docvecs.doctags))
#print(model.raw_vocab)

while True:
	sys.stdout.write("input title: ")
	title = input()
	if title == "show titles":
		text = "\n".join(str(x) for x in model.docvecs.doctags.keys())
		print(text)
		continue
	if title in model.docvecs.doctags:
		result = model.docvecs.most_similar(title, topn = 10)
		text = "\n".join(str(x) for x in result)
		print(text)
	else:
		print("not match")
