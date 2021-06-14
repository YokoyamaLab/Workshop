# リード文はtourist_spot.jsonを参照

import MeCab
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import json
import math

# 特定の品詞を抽出する
def extraction(node,word_list,select):
    while node:
        word_type = node.feature.split(',')[0]
        if select == 'noun' and word_type == '名詞':
            word_list.append(node.surface)
        elif select == 'all':
            word_list.append(node.surface)
        node = node.next
    return word_list

# コーパスづくりと平均を求める
def create_corpus(data):
    corpus = []
    sum = 0
    for spot in data.values():
        lead = spot['lead']
        if lead == None:
            continue

        # MeCabの準備
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(lead)

        # 特定の品詞を取り出す
        tmp_list = []
        word_list = []
        select = 'all'
        word_list = extraction(node,tmp_list,select)
        sum += len(word_list)
        word_chain = ' '.join(word_list) # リストを文字列に変換
        corpus.append(word_chain)
    avgdl = sum / len(corpus)
    return corpus, avgdl

# def mytfidf(word_list,corpus):
#     word_list_checked = []
#     word_count = 0
#     tfidf_dict = {}
#     for word in word_list:
#         if word in word_list_checked:
#             continue
#         else:
#             word_list_checked.append(word)
#             word_count = word_list.count(word)
#         tf = word_count / len(word_list)
#         idf = calc_idf(word,corpus)
#         tfidf_dict[word] = tf*idf
#     return tfidf_dict

# TF-IDFやBM25を求める
def calc(word_list,corpus,avgdl,mode):
    word_list_checked = []
    word_count = 0
    dict = {}
    for word in word_list:
        if word in word_list_checked:
            continue
        else:
            word_list_checked.append(word)
            word_count = word_list.count(word)
        d = len(word_list)
        tf = word_count / d
        idf = calc_idf(word,corpus)
        k1 = 2.0
        b = 0.75
        if mode == 'TFIDF':
            dict[word] = tf*idf
        elif mode == 'BM25':
            dict[word] = idf*(tf*k1+1)/(tf+k1*(1-b+b*d/avgdl))
    return dict

# IDFを求める
def calc_idf(word, corpus):
    dft = 0
    for check in corpus:
        if word in check:
            dft+=1
    # print(str(dft)+' '+word)
    idf = math.log(len(corpus)/dft,2)
    return idf

def main():
    src = open('tourist_spot.json', 'r',encoding='utf-8')
    data = json.load(src)
    corpus, avgdl = create_corpus(data)

    for spot in data.values():
        title = spot['title']
        lead = spot['lead']
        if lead == None:
            continue

        # MeCabの準備
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(lead)

        select = 'all' # all or noun
        mode = 'BM25' # TFIDF or BM25 or None
        word_list = []
        word_list = extraction(node,word_list,select)

        if mode == 'TFIDF' or mode == 'BM25':
            word_dict = calc(word_list,corpus,avgdl,mode)
            Wc = WordCloud(width=640, height=480, background_color='white', colormap='tab20', font_path='C:\Windows\Fonts\yumin.ttf').generate_from_frequencies(word_dict)
        else:
            word_chain = ' '.join(word_list)
            Wc = WordCloud(width=640, height=480, background_color='white', colormap='tab20', font_path='C:\Windows\Fonts\yumin.ttf').generate_from_text(word_chain)

        plt.imshow(Wc)
        plt.axis('off')
        # plt.show()
        if mode == 'TFIDF':
            filename = 'img/'+title+'/TFIDF'
        elif mode == 'BM25':
            filename = 'img/'+title+'/BM25'
        elif select == 'noun':
            filename = 'img/'+title+'/noun'
        elif select == 'all':
            filename = 'img/'+title+'/all_word_class'
        plt.savefig(filename)
        print('save '+ title + ' ' + select + ' ' + mode + ' img' )

if __name__ == "__main__":
    main()
