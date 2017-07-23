from __future__ import division
from nltk import ngrams
from stemming.porter2 import stem
import time
import os
import sys
import math
import pstats 

def n_grams(n,string):
    str_ngrams = []
    Ngrams = ngrams(string.split(),n)
    for grams in Ngrams:
    	str_grams = ''
    	for gram in grams:
    		str_grams += ( ' ' + stem(gram))
    	str_ngrams.append(str_grams)
    return str_ngrams
	
def count_pos():
	path = './training_data/pos/'
	cpos = 0
	for filename in os.listdir(path):
		cpos = cpos + 1
	return cpos

def count_neg():
	path = './training_data/neg/'
	cneg = 0
	for filename in os.listdir(path):
		cneg = cneg + 1
	return cneg

def mega_pos():
	path = './training_data/pos/'
	fmegaPos = ''
	for filename in os.listdir(path):
		content = '' 
		with open(path+filename, 'r') as content_file:
			content = content_file.read()
		fmegaPos = fmegaPos + ' ' + content
	return fmegaPos

def mega_neg():

	path = './training_data/neg/'
	fmegaNeg = ''
	for filename in os.listdir(path):
		content = '' 
		with open(path+filename, 'r') as content_file:
			content = content_file.read()
		fmegaNeg = fmegaNeg + ' ' + content
	return fmegaNeg

def vocabulary(string):
	voc = list(set(string))
	return voc

def occurrences(word,mega):
	return mega.count(word)

def dict_occernces_mega_pos(mega_pos):
	pos_occur = {}
	mega_pos_voc = vocabulary(mega_pos)
	for word in mega_pos_voc:
		pos_occur[word] = occurrences(word,mega_pos)
	return pos_occur

def dict_occernces_mega_neg(mega_neg):
	neg_occur = {}
	mega_neg_voc =  vocabulary(mega_neg)
	for word in mega_neg_voc:
		neg_occur[word] = occurrences(word,mega_neg)
	return neg_occur

def get_occerns(mega_dict,word):
	if word in mega_dict.keys():
		return mega_dict[word]
	else:
		return 0
 
def sentence_probablity(voc_testFile,mega_pos,mega_neg,pos_probabilty
	,neg_probalilty,length_mega_pos,length_voc_mega_pos,length_mega_neg,length_voc_mega_neg,pos_dict,neg_dict):
	#neg =0 , pos =1 
	result = 0 

	#porbablity pos mega 
	pos_den = (length_mega_pos+length_voc_mega_pos)
	pos = math.log(pos_probabilty)
	for word in voc_testFile:
		word_occur = get_occerns(pos_dict,word)
		word_probabilty = (word_occur+1)/pos_den
		pos += math.log(word_probabilty)

	#probablity neg mega  
	neg_den = (length_mega_neg+length_voc_mega_neg)
	neg = math.log(neg_probalilty)
	for word in voc_testFile:
		word_occur = get_occerns(neg_dict,word)
		word_probabilty = (word_occur+1)/neg_den
		neg += math.log(word_probabilty)

	if pos>neg:
		result = 1
	return result

def F1(precision,recall):
	return (2*precision*recall)/(precision+recall)

def precision(tp,fp):
	return tp/(tp+fp)

def recall(tp,fn):
	return tp/(tp+fn)

def acrucy(tp,fp,tn,fn):
	return tp/(tp+fp+tn+fn)

def main():

	cpos = count_pos()
	cneg = count_neg()
	pos_probabilty = float((cpos/(cpos+cneg)))
	neg_probalilty = float(cneg/(cpos+cneg))
	
	n = 1

	mega_start= time.time()
	fmegapos = n_grams(n,mega_pos())
	fmeganeg = n_grams(n,mega_neg())
	mega_end = time.time()
	print mega_end - mega_start

	dict_start_neg = time.time()
	neg_dict = dict_occernces_mega_neg(fmeganeg)
	dict_end_neg = time.time()
	print( dict_end_neg - dict_start_neg)
	dict_start_pos = time.time()
	pos_dict = dict_occernces_mega_pos(fmegapos)
	dict_end_pos = time.time()
	print( dict_end_pos - dict_start_pos)
	

	'''
	#create mega Files 
	if os.path.exists('./mega_pos_'+str(n)+'.txt'):
		fmegapos = list(open('./mega_pos_'+str(n)+'.txt','r').read())
	else:
		f = open('./mega_pos_'+str(n)+'.txt', "w")
		f.write(str(n_grams(n,mega_pos())))

	
	if os.path.exists('./mega_neg_'+str(n)+'.txt'):
		fmeganeg = list(open('./mega_neg_'+str(n)+'.txt','r').read())
	else:
		f = open('./mega_neg_'+str(n)+'.txt', "w")
		f.write(str(n_grams(n,mega_neg())))

	'''

	length_voc_mega_neg =len(vocabulary(fmeganeg))
	length_mega_neg = len(fmeganeg)

	length_voc_mega_pos = len(vocabulary(fmegapos))
	length_mega_pos = len(fmegapos)

	'''
	eva_start = time.time()
	test_file = open('./test_data/pos/cv000_29590.txt','r').read()
	check_file = vocabulary(n_grams(n,test_file))
	res = sentence_probablity(n_grams(n,test_file),fmegapos,fmeganeg,pos_probabilty
		,neg_probalilty,length_mega_pos,length_voc_mega_pos,length_mega_neg,length_voc_mega_neg,pos_dict,neg_dict)
	eva_end = time.time()
	print eva_end- eva_start
	'''

	tp = 0
	fp = 0
	fn = 0
	tn = 0

 	pos_eval_start=time.time()
	pos_path =  './test_data/pos/'
	for filename in os.listdir(pos_path):
		test_file = open(pos_path+filename,'r').read()
		check_file = vocabulary(n_grams(n,test_file))
		res = sentence_probablity(n_grams(n,test_file),fmegapos,fmeganeg,pos_probabilty
			,neg_probalilty,length_mega_pos,length_voc_mega_pos,length_mega_neg,length_voc_mega_neg,pos_dict,neg_dict)
		#print('file: ',filename,' DONE ,reslut :',res)
		if res == 1:
			tp = tp +1
		if res == 0:
			fn = fn +1 
	pos_eval_end=time.time()
	print(pos_eval_end- pos_eval_start)

	neg_eval_start = time.time()
	neg_path =  './test_data/neg/'
	for filename in os.listdir(neg_path):
		test_file = open(neg_path+filename,'r').read()
		check_file = vocabulary(n_grams(n,test_file))
		res = sentence_probablity(n_grams(n,test_file),fmegapos,fmeganeg,pos_probabilty
			,neg_probalilty,length_mega_pos,length_voc_mega_pos,length_mega_neg,length_voc_mega_neg,pos_dict,neg_dict)
		#print('file: ',filename,' DONE,reslut :',res)
		if res == 0:
			tn = tn +1 
		if res == 1:
			fp = fp +1
	neg_eval_end = time.time()

	print(neg_eval_end- neg_eval_start)
	
	print(precision(tp,fp))
	print(recall(tp,fn))
	print(acrucy(tp,fp,tn,fn))
	print(F1(precision(tp,fp),recall(tp,fn)))
	
	pass
if __name__ == '__main__':
	main()
