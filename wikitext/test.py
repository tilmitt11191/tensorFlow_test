#from gensim.models import word2vec
from os import listdir, path

list = list("1234")
files = [path.join("./text", x) for x in list]
print(str(files))
print(path)

"""
def corpus_files():
    dirs = [path.join('./text', x)
            for x in listdir('./text') if not x.endswith('.txt')]
    docs = [path.join(x, y)
            for x in dirs for y in listdir(x) if not x.startswith('LICENSE')]
    return docs
"""