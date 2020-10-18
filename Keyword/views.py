import time

from django.http import HttpResponse

from Keyword.dao import get_df, get_review, read_all, update_df
from Keyword.service import df, tfidf, count, phrase, get_stop, df_phrase, tfidf_phrase, get_punc, get_phrase

e = 10
stop = get_stop()
punc = get_punc()

def weight(request):
    start = time.process_time()
    count(0, e)
    # time consuming
    end = time.process_time()
    time_used = (end - start) / 60000  # ms--->min
    return HttpResponse(time_used)


def keyword(request):
    df_dic = get_df()
    review = get_review(0)
    num_doc = e * 10000
    keyword = tfidf(review, df_dic, num_doc)
    print(keyword)
    return HttpResponse(review)


def weight_phrase(request):
    start = time.process_time()
    review_list = read_all(0)
    df_dic = get_df(1)
    for review in review_list:
        df_phrase(review, punc, stop, df_dic)
    update_df(df_dic, 1)

    # time consuming
    end = time.process_time()
    time_used = (end - start) / 60000  # ms--->min
    return HttpResponse(time_used)


def key_phrase(request):
    df_dic = get_df(1)
    review = get_review(0)
    num_doc = 10000
    keyword = tfidf_phrase(review, df_dic, num_doc, punc, stop)
    print(keyword)
    return HttpResponse(review)


def test(request):
    review = get_review(0)
    # phrase_list = phrase(review, punc, stop)
    # get_phrase(review)
    update_df({}, 1)
    return HttpResponse(e)