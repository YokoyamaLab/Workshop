# https://qiita.com/kyoro1/items/59216cc09b56d5b5f760
# https://analytics-note.xyz/programming/frequencies-word-cloud/

import pandas as pd
import csv
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import gensim
import math
import numpy as np

fpath = "~/Library/Fonts/RictyDiminished-for-Powerline/RictyDiminished-Bold.ttf"

## データ読み込み
#df = pd.read_csv('sample.csv', header=None)
## タイトルを付与
#df.columns = ['sentences']

csv_file = "wikidata2_hand.csv"

t = Tokenizer()
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = None
dictionary = None
## 関数群の定義
def get_nouns(sentence, noun_list):
    for token in t.tokenize(sentence):
        split_token = token.part_of_speech.split(',')
        ## 一般名詞を抽出
        if split_token[0] == '名詞' and split_token[1] == '一般':
            noun_list.append(token.surface)

def depict_word_cloud_freq(title,noun_list):
    ## 名詞リストの要素を空白区切りにする(word_cloudの仕様)
    noun_space = ' '.join(map(str, noun_list))
    ## word cloudの設定(フォントの設定)
    wc = WordCloud(background_color="white",font_path=fpath, width=300,height=300)
    wc.generate(noun_space)
    ## 出力画像の大きさの指定
    fig = plt.figure(figsize=(5,5))
    ## 目盛りの削除
    plt.tick_params(labelbottom=False,
                    labelleft=False,
                    labelright=False,
                    labeltop=False,
                   length=0)
    ## word cloudの表示
    plt.imshow(wc)
    #plt.show()
    fig.savefig('./img/'+title+'_freq.png')

# https://tech.enigmo.co.jp/entry/2018/12/19/112837
def depict_word_cloud_tfidf(title,noun_list):
    
    words_vectornumber = {}
    for k,v in sorted(vectorizer.vocabulary_.items(), key=lambda x:x[1]):
        words_vectornumber[v] = k
    vecs_array = vecs.toarray()
    all_reports = []
    vecs_dic = {}
    
    for vec in vecs_array:
        words_report = []
        vector_report = []
        for i in vec.nonzero()[0]:
            vecs_dic[words_vectornumber[i]] = vec[i]
    wc_1 = WordCloud(
        font_path=fpath,
        width=600,
        height=300,
        prefer_horizontal=1,
        background_color='white',
        include_numbers=True,
        colormap='tab20',
    ).generate_from_frequencies(vecs_dic)

    ## 出力画像の大きさの指定
    fig = plt.figure(figsize=(5,5))
    ## 目盛りの削除
    plt.tick_params(labelbottom=False,
                    labelleft=False,
                    labelright=False,
                    labeltop=False,
                   length=0)
    ## word cloudの表示
    plt.imshow(wc_1)
    #plt.show()
    fig.savefig('./img/'+title+'_tfidf.png')

# https://qiita.com/d-ogawa/items/c423cd4b01c6ed84a5e7
def depict_word_cloud_lda(title,noun_list):
    
    #dictionary.filter_extremes(no_below=3, no_above=0.5)
    corpus = [dictionary.doc2bow(t) for t in noun_list]
    # LDA
    num_topics = 10
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                random_state=0)
    ## 出力画像の大きさの指定
    fig = plt.figure(figsize=(5,5))
    #ncols = math.ceil(num_topics/2)
    #nrows = math.ceil(lda_model.num_topics/ncols)
    #fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15,7))
    ## 目盛りの削除
    plt.tick_params(labelbottom=False,
                    labelleft=False,
                    labelright=False,
                    labeltop=False,
                   length=0)
    ## word cloudの表示
    #for i,t in enumerate(range(lda_model.num_topics)):
    x = dict(lda_model.show_topic(1, 30))
    wc = WordCloud(
        font_path=fpath,
        width=600,
        height=300,
        prefer_horizontal=1,
        background_color='white',
        include_numbers=True,
        colormap='tab20',
    ).generate_from_frequencies(x)
    #    axs[i].imshow(wc)
    #    axs[i].axis('off')
    #    axs[i].set_title('Topic '+str(t))
    plt.imshow(wc)
    #plt.show()
    #plt.tight_layout()
    plt.savefig('./img/'+title+'_lda.png')


def main():
    f = open(csv_file,'r')
    reader = csv.reader(f)
    learn_list = []
    for row in reader:
        for sentence in row:
            get_nouns(sentence, learn_list)
    vecs = vectorizer.fit_transform(learn_list)
    dictionary = gensim.corpora.Dictionary(learn_list)
    f.close()
    # cnt = 0
    f = open(csv_file,'r')
    reader = csv.reader(f)
    for row in reader:
        noun_list = []
        for sentence in row:
            get_nouns(sentence, noun_list)
        #print(noun_list)
        
        depict_word_cloud_freq(row[0],noun_list)
        depict_word_cloud_tfidf(row[0],noun_list)
        depict_word_cloud_lda(row[0],[noun_list])
    
    f.close()

    # noun_list = []
    # for sentence in list(df['sentences']):
    #     print(sentence)
    #     get_nouns(sentence, noun_list)
    
    
    # depict_word_cloud_freq("test",noun_list)

if __name__ == "__main__":
    main()

