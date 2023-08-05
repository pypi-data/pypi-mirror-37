# -*- coding: utf-8 -*-
# @Time    : 18-9-28 下午1:47
# @Author  : duyongan
# @FileName: text_utils.py
# @Software: PyCharm
import re
from simple_pickle import utils
from jieba import posseg
from text_process.text import Text
import nltk
import os
import numpy as np

def text2sencents_zh(text):
    text = re.sub('\u3000|\r|\t|\xa0', '', text)
    text = re.sub('？”|！”|。”', '”', text)
    sentences = re.split("([。！？……])", text)
    sentences.append('')
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    last_sentences=[]
    for sentence in sentences:
        last_sentences+=[senten.replace('\n','').strip() for senten in sentence.split('\n\n')
                         if senten.replace('\n','').strip()]
    return last_sentences

def text2sencents_en(text):
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    return sentences


def sort_keys_weights(keys,weights,return_tuple=False):
    keys_weights = dict(zip(keys, weights))
    keys_weights = sorted(keys_weights.items(), key=lambda k: k[1], reverse=True)
    if return_tuple:
        return keys_weights
    keys = [term[0] for term in keys_weights]
    return keys

def text_process_zh_single(text):
    here = os.path.dirname(__file__)
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    stopwords=utils.read_pickle(here+'/stopwords')
    text=posseg.lcut(text)
    text_n_list = [word_.word for word_ in text if
                   len(word_.word) > 1 and word_.word not in stopwords and
                   word_.flag in ['n','v','ns','nt','nr','ni','nl','nz',
                                  'nrf','nsf','nrj','nr1','nr2']]
    return text_n_list

def text_process_zh_not_single(text):
    here = os.path.dirname(__file__)
    stopwords = utils.read_pickle(here+'/stopwords')
    words = [tuple_ for tuple_ in list(posseg.cut(text))
             if list(tuple_)[0].strip() and len(list(tuple_)[0].strip())>1]
    words2 = []
    temp = ''
    enstart = False
    for i in range(len(words)):
        if words[i].flag in ['n','ns','nt','nr','ni','nl',
                             'nz','nrf','nsf','nrj','nr1',
                             'nr2'] and len(temp) <3 and not enstart:
            if words[i].word not in stopwords:
                temp = temp + words[i].word
            if i == len(words) - 1:
                if temp.strip() != '':
                    words2.append(temp)
        else:
            if temp.strip() != '' and not enstart:
                words2.append(temp)
                temp = ''
    return words2

def text_process_en(text):
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    text = text.replace(',', ' ')
    text_list = text.split()
    texter = Text(text_list)
    text_n_list = texter.collocations()
    return text_n_list

def range_easy(a_object):
    return range(len(a_object))

def duplicate(a_list):
    return list(set(a_list))

def getKeywords_zh_single(text,num=5):
    here = os.path.dirname(__file__)
    idf_map = utils.read_pickle(here + '/idf_map')
    moshengci_weight = max(idf_map.values())
    text_n_list=text_process_zh_single(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set,keywords_weight)[:min(num, len(keywords_set))]

def getKeywords_zh_not_single(text,num=5):
    here = os.path.dirname(__file__)
    idf_map = utils.read_pickle(here + '/idf_map')
    moshengci_weight = max(idf_map.values())
    text_n_list=text_process_zh_not_single(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set,keywords_weight)[:min(num, len(keywords_set))]

def getKeywords_en(text,num=5):
    here = os.path.dirname(__file__)
    idf_map = utils.read_pickle(here + '/idf_map')
    moshengci_weight = max(idf_map.values())
    text_n_list=text_process_en(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set,keywords_weight)[:min(num, len(keywords_set))]

def compare_two_txt(text1,text2):
    words1 = text_process_zh_single(text1)
    words2 = text_process_zh_single(text2)
    same_len=len([val for val in words1 if val in words2])
    return (same_len/len(words1)+same_len/len(words2))/2

def cos(i,j):
    return np.nan_to_num(np.dot(i, j) / (np.linalg.norm(i) * np.linalg.norm(j)))


class compare_bot:
    def __init__(self):
        self.__here = os.path.dirname(__file__)
        self.__single_word2vec = utils.read_pickle(self.__here + '/single_word2vec')
    def compare_two_txt_accuracy(self,text1,text2):
        words1 = getKeywords_zh_single(text1, 20)
        words2 = getKeywords_zh_single(text2, 20)
        vec1 = []
        for word in words1:
            for w in list(word):
                try:
                    vec1.append(self.__single_word2vec[w])
                except:
                    pass
        vec1 = np.sum(vec1, axis=0) / max(len(vec1),0.9999)
        vec2 = []
        for word in words2:
            for w in list(word):
                try:
                    vec2.append(self.__single_word2vec[w])
                except:
                    pass
        vec2 = np.sum(vec2, axis=0) / max(len(vec2),0.9999)
        result=cos(vec1, vec2)
        if type(result) != np.float64:
            result = 0.0
        return result
    def compare_two_word(self,word1,word2):
        vec1 = []
        for w in list(word1):
            try:
                # print(single_word2vec[w])
                vec1.append(self.__single_word2vec [w])
            except:
                pass
        vec1 = np.sum(vec1, axis=0) / max(len(vec1), 0.9999)
        vec2=[]
        for w in list(word2):
            try:
                vec2.append(self.__single_word2vec [w])
            except:
                pass
        vec2 = np.sum(vec2, axis=0) / max(len(vec2), 0.9999)
        result = cos(vec1, vec2)
        if type(result) != np.float64:
            result = 0.0
        return result

# def compare_two_txt_accuracy(text1,text2):
#     words1 = getKeywords_zh_single(text1,20)
#     words2 = getKeywords_zh_single(text2,20)
#     here = os.path.dirname(__file__)
#     single_word2vec = utils.read_pickle(here + '/single_word2vec')
#     vec1 = []
#     for word in words1:
#         for w in list(word):
#             try:
#                 vec1.append(single_word2vec[w])
#             except:
#                 pass
#     vec1=np.sum(vec1,axis=0)/max(len(vec1),0.9999)
#     vec2 = []
#     for word in words2:
#         for w in list(word):
#             try:
#                 vec2.append(single_word2vec[w])
#             except:
#                 pass
#     vec2=np.sum(vec2,axis=0)/max(len(vec2),0.9999)
#     result = cos(vec1, vec2)
#     if type(result) != np.float64:
#         result = 0
#     return result


def getAbstract_zh(title,text,num=3):
    # compare_botor=compare_bot()
    sentences=text2sencents_zh(text)
    vecs_sim = []
    for sentence in sentences:
        vecs_sim.append(compare_two_txt(title, sentence))
        # vecs_sim.append(compare_botor.compare_two_txt_accuracy(title, sentence))
    abstract=sort_keys_weights(sentences,vecs_sim)[:min(num, len(sentences))]
    index_num=[sentences.index(sentence) for sentence in abstract]
    abstract = sort_keys_weights(abstract, index_num)
    return ''.join(abstract)

def getAbstract_en(title,text,num=3):
    sentences=text_process_en(text)
    vecs_sim = []
    for sentence in sentences:
        vecs_sim.append(compare_two_txt(title, sentence))
    abstract=sort_keys_weights(sentences,vecs_sim)[:min(num, len(sentences))]
    index_num=[sentences.index(sentence) for sentence in abstract]
    abstract = sort_keys_weights(abstract, index_num)
    return ''.join(abstract)



# title='安徽北京'
# text="安徽上海"
# # # print(get_nlp_hash_code_zh(text))
# # # print(getAbstract_zh(title,text))
# # print(compare_two_word(text,title))
# compare_botor=compare_bot()
# # # # text2='安徽'
# print(compare_botor.compare_two_txt_accuracy(text,title))
# print(compare_botor.compare_two_word(text,title))