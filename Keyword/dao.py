from .models import Df, Review, Text, Tf


def read_all(start):
    review_list = []
    for i in range(10000):
        try:
            review_list.append(Review.objects[10000 * start+i].text)
        except IndexError:
            break
    return review_list


def save_keyword(index, keyword_list):
    review = Review.objects[index]
    review.keyword = keyword_list
    review.save()


def get_df(index = 0):
    df = Df.objects[index]
    return df.df_dic


def update_df(df_dic, index = 0):
    df = Df.objects[index]
    df.df_dic = df_dic
    df.save()


def save_tf(tf_dic):
    Tf(tf_dic = tf_dic).save()


def get_tf_all():
    tf_list = []
    for tf in Tf.objects:
        tf_list.append(tf.tf_dic)
    return tf_list


def get_tf(index):
    return Tf.objects[index].tf_dic


def get_review(index):
    return Review.objects[index].text
