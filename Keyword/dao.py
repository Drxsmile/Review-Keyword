from .models import Review, Text, Df, Tf


def read_all():
    review_list = []
    for review in Review.objects:
        # 先读取这些
        if len(review_list) == 10000:
            break
        review_list.append(review.text)
    return review_list


def save_keyword(index, keyword_list):
    review = Review.objects[index]
    review.keyword = keyword_list
    review.save()


def get_df():
    df_dic = Df.objects[0].df_dic
    return df_dic


def update_df(df_dic):
    df = Df.objects[0]
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

