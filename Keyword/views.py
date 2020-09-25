import math

from django.http import HttpResponse
from django.shortcuts import render
from .models import Text, Review
import nltk
import string
from nltk.corpus import stopwords, wordnet
import nltk.stem
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.text import TextCollection


# Create your views here.

def clean(request):
    for review in Review.objects:
        # 小写和去除标点
        lower = review.text.lower()
        remove = str.maketrans('', '', string.punctuation)
        without_punctuation = lower.translate(remove)
        # 得到分词列表
        tokens = word_tokenize(without_punctuation)
        # 去除stopwords
        without_stopwords = [w for w in tokens if not w in stopwords.words('english')]

        # 获取单词词性并还原单词
        tagged = pos_tag(without_stopwords)  # [('单词', '词性')，……]
        wnl = WordNetLemmatizer()
        lemmas_words = []
        for tag in tagged:
            wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
            lemmas_words.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原
        review.words = lemmas_words

        # 提取词干得到清洗后数据
        # s = nltk.stem.SnowballStemmer('english')
        # review.words = [s.stem(ws) for ws in without_stopwords]

        # 存入数据库
        review.save()
    return HttpResponse("split into words success")


# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def count(request):
    # 构建语料库
    data = []
    for review in Review.objects:
        data.append(review.words)
    corpus = TextCollection(data)

    # 统计tf_idf
    for review in Review.objects:
        dic = {}  # word : tfidf
        wordlist = review.words
        for word in wordlist:
            dic[word] = corpus.tf_idf(word, corpus)
        review.tfidf = sorted(dic.items(), key = lambda x:x[1],reverse = True)
        tfidflist = review.tfidf
        temp = tfidflist[:5]
        keylist = []
        for tup in temp:
            keylist.append(tup[0])
        review.keyword = keylist
        review.save()
    return HttpResponse("count term frequency success")


def weight(request):
    # 语料库
    data = []
    for review in Review.objects:
        data.append(review.words)

    # df
    words = []
    for wordlist in data:
        words += wordlist
    words = set(words)
    df_dic = {}
    for word in words:
        for wordlist in data:
            if word in wordlist:
                if word in df_dic:
                    df_dic[word] += 1
                else:
                    df_dic[word] = 1
    # idf
    idf_dic = {}
    num_doc = len(data)
    for k, v in df_dic.items():
        idf_dic[k] = math.log(num_doc/v)

    # tf & tfidf
    # tf_list = []
    tfidf_list = []
    for wordlist in data:
        tf_dic = {}
        for word in wordlist:
            if word in tf_dic:
                tf_dic[word] += 1
            else:
                tf_dic[word] = 1
        tf_max = max(tf_dic.values())
        # doc_len = len(wordlist)
        tfidf_dic = {}
        for k, v in tf_dic.items():
            # tf_dic[k] = v / tf_max
            # tf_dic[k] = v / doc_len
            tfidf_dic[k] = v / tf_max * idf_dic[k]
        # tf_list.append(tf_dic)
        tfidf_list.append(tfidf_dic)
    # database
    i = 0
    for review in Review.objects:
        review.tf_idf = sorted(tfidf_list[i].items(), key=lambda x: x[1], reverse=True)
        tfidflist = review.tf_idf
        temp = tfidflist[:5]
        keylist = []
        for tup in temp:
            keylist.append(tup[0])
        review.key_word = keylist
        review.save()
        i += 1
    return HttpResponse("weight success")

def test(request):
    print(len(Text.objects))
    print(Text.objects[0]) # 不行
    return HttpResponse('success')