
import codecs
import re

from gensim import models
from gensim.models.doc2vec import LabeledSentence

sentences = []

def contents_to_sentences(title, contents):
	print("title: " + str(title.encode("utf-8")))
	print("len(sentences): " + str(len(sentences)))
	sentences.append(LabeledSentence(words=contents, tags=[title]))

f = codecs.open(
	"../../data/wikitext/wikitext-103-raw/wiki.train.raw", "r", "utf-8")
title = ""
contents = ""
for row in f:
	if re.findall(r"^\s=\s[^=]", row):
		# this line means new title. add old title and contents to sentences.
		if title != "":
			contents_to_sentences(title, contents)
		title = re.sub(r"^\s=\s|\s=\s\n$", "", row)
		contents = ""
	else:
		contents += row
# add last title and contents to sentences.
contents_to_sentences(title, contents)
print("create sentences finished. close file")
f.close()

print("create model")
model = models.Doc2Vec(
	sentences, dm=0, size=300, window=15, alpha=.025,
	min_alpha=.025, min_count=1, sample=1e-6)

print('\ntrain start')
for epoch in range(20):
	print('Epoch: {}'.format(epoch + 1))
	model.train(sentences,  total_examples=len(sentences), epochs=model.iter)
	model.alpha -= (0.025 - 0.0001) / 19
	model.min_alpha = model.alpha

print("save model")
model.save('wikitext_doc2vec.model')
#model = models.Doc2Vec.load('wikitext_doc2vec.model')