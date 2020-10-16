import time
import weakref
from django.http import HttpResponse

from Keyword.dao import read_all, get_df, update_df, get_tf_all
from Keyword.models import Review
from Keyword.service import df, tfidf

# 从数据库中读取
review_list = read_all()
num_doc = len(review_list)


def weight(request):
    start = time.process_time()
    df_dic = get_df()
    for i in range(num_doc):
        df_new = df(review_list[i], df_dic)
        update_df(df_new)
    # tf_list = get_tf_all()
    # for i in range(len(tf_list)):
    #     tfidf(tf_list[i], df_dic, num_doc, i)

    # time consuming
    end = time.process_time()
    time_used = (end - start) / 60000  # ms--->min
    return HttpResponse(time_used)


def keyword(request):
    df_dic = get_df()
    review = Review.objects[0].text
    keyword = tfidf(review, df_dic, num_doc)
    print(keyword)
    return HttpResponse(review)


def test(request):
    x = 4
    # print(len(Text.objects))
    # df = {"some" : 2, "sum" : 3}
    # Df(df_dic = df).save()

    # df = Df.objects[0]
    # df.df_dic = {}
    # df.save()
    # update_df({})
    df_dic = get_df()
    print(df_dic)
    # print(Text.objects[0].text)
    return HttpResponse(x)