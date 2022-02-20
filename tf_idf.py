import nltk
import os
import json
import math
from spell import correctSentence
from indexcreate import lemmatize_sentence


def Cal_query_tf_idf(inputwords,invertedindex):
    query_tfidf={}
    for word in inputwords:
        if word in invertedindex:
            if word not in query_tfidf:
                query_tfidf[word] = {}
                query_tfidf[word]["tf"] = 1
                query_tfidf[word]["df"] = len(invertedindex[word])
            else:
                query_tfidf[word]["tf"] += 1
    doc_length = 0
    for word in query_tfidf:
        tf = query_tfidf[word]["tf"]/len(query_tfidf)
        df = query_tfidf[word]["df"]
        tf_idf = Caclu_tf_idf(tf, df, 10788)
        query_tfidf[word]["nomalized"] = tf_idf
        doc_length += math.pow(tf_idf, 2)
    doc_length = math.sqrt(doc_length)
    for word in query_tfidf:
        tf_idf = query_tfidf[word]["nomalized"]
        query_tfidf[word]["nomalized"] = tf_idf / doc_length
    return query_tfidf


def build_tf_idf(root_dir="./Reuters"):
    dict = {}
    with open("./dictionary/invertedIndex.json","r") as f:
        invertedIndex=json.load(f)
    file_names = [os.path.join(root_dir, i) for i in os.listdir(root_dir)]
    N=len(file_names)
    for file_name in file_names:
        doc_id = file_name.split("\\")[1][:-5]
        dict[doc_id]={}
        with open(file_name, "r") as f:
            print("正在处理文件：", file_name)
            lines = f.read()
            sentences = lemmatize_sentence(lines,False)
            sum_word = len(sentences)
            for word in sentences:
                if word not in dict[doc_id]:
                    dict[doc_id][word] = {}
                    dict[doc_id][word]["tf"]=len(invertedIndex[word][doc_id])/sum_word
                    dict[doc_id][word]["df"]=len(invertedIndex[word])
                else:
                    continue
        doc_length=0
        for word in dict[doc_id]:
            tf=dict[doc_id][word]["tf"]
            df=dict[doc_id][word]["df"]
            tf_idf=Caclu_tf_idf(tf,df,N)
            dict[doc_id][word]["nomalized"]=Caclu_tf_idf(tf,df,N)
            doc_length+=math.pow(tf_idf,2)
        doc_length=math.sqrt(doc_length)
        for word in dict[doc_id]:
            dict[doc_id][word]["nomalized"]=dict[doc_id][word]["nomalized"]/doc_length
    with open("./dictionary/nomalized_tf_idf.json","w") as f:
        json.dump(dict,f)


def Caclu_tf_idf(tf,df,N):
    result=tf*math.log10(N/df)
    return result

if __name__=="__main__":
    build_tf_idf()