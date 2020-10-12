import math
import string

from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

from Keyword.dao import save_keyword, save_tf


def clean(review):
    # 小写和去除标点
    lower = review.lower()
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
    return lemmas_words
    # 提取词干得到清洗后数据
    # s = nltk.stem.SnowballStemmer('english')
    # review = [s.stem(ws) for ws in without_stopwords]


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


def df(review, df_dic):
    wordlist = clean(review)
    wordlist_set = set()
    # tf_dic = {}
    for word in wordlist:
        # word frequency
        # if word in tf_dic:
        #     tf_dic[word] += 1
        # else:
        #     tf_dic[word] = 1
        # df
        if word not in wordlist_set:
            wordlist_set.add(word)
            if word in df_dic:
                df_dic[word] += 1
            else:
                df_dic[word] = 1
    # save_tf(tf_dic)


def tfidf(review, df_dic, num_doc):
    wordlist = clean(review)
    tf_dic = {}
    for word in wordlist:
        # word frequency
        if word in tf_dic:
            tf_dic[word] += 1
        else:
            tf_dic[word] = 1
    tf_max = max(tf_dic.values())
    tfidf_dic = {}
    for k, v in tf_dic.items():
        tfidf_dic[k] = v / tf_max * math.log(num_doc / df_dic[k])
    tfidf_sorted = sorted(tfidf_dic.items(), key=lambda x: x[1], reverse=True)
    temp = tfidf_sorted[:5]
    keyword_list = []
    for tup in temp:
        keyword_list.append(tup[0])
    return keyword_list

