import re
import xml.etree.ElementTree as ET

#XmlData = "sample_enwiki_pages_article.txt"
XmlData = "../../data/wikitext/enwiki-20170501-pages-articles1.xml-p10p30302"
path = "../../data/wikitext/contents/"

def get_title_and_contents_of(page):
	title = ""
	contents = ""
	if page is None:
		print("page is none")
		return "", ""
	for el in list(page):
		if re.match(".*redirect$", el.tag):
			return "", ""
		if re.match(".*title$", el.tag):
			title = el.text
		if re.match(".*revision$", el.tag):
			contents = get_contents_of(el)
	return title, contents

p = re.compile(r"<[^>]*?>|\[\[|\]\]|{{[^>]*?}}", flags=re.DOTALL)

def get_contents_of(revision):
	contents = "aaa"
	for el in revision:
		if re.match(".*text$", el.tag):
			return p.sub("", el.text)
	return contents

root = ET.parse(XmlData).getroot()
pages = [el for el in list(root) if re.match(".*page$", el.tag)]

times = 1
num = len(pages)
for page in pages:
	print("times[" + str(times) + "] num[" + str(num) + "]")
	title, contents = get_title_and_contents_of(page)
	if title != "Con" and title != "" and contents != "":
		f = open(path + re.sub(r"/|:|\?|.|\*", "", title) + ".txt", "w")
		f.write(contents.replace("\n", ""))
		f.close
	times += 1

#for e in list(root):
#	print(e.tag)

"""
from xml.dom import minidom

def getText(nodeList):
	rc = ""
	for node in nodeList:
		if node.nodeType == node.TEXT_NODE:
			rc += node.data
	return rc

xdoc = minidom.parse("sample_enwiki_pages_article.txt")

pages = [xdoc.getElementsByTagName("page")[0]]
print(len(pages))
for page in pages:
	#print(dir(page))
	print(getText(page.getElementsByTagName("title")[0].childNodes))
"""