from Heap_sort import heap_sort
from colorama import init
init(autoreset=True)
from tf_idf import Cal_query_tf_idf
from spell import correctSentence
from BoolSearchDel import lemmatize_sentence
import queue
from BoolSearchDel import searchOneWord,mergeTwoList

#仅计算包含这些词语的并集

def get_cos_score(query_tf_idf,tf_idf,doc_id):
   score=0
   for word in query_tf_idf:
      if word in tf_idf[str(doc_id)]:
         score=score+query_tf_idf[word]["nomalized"]*tf_idf[str(doc_id)][word]["nomalized"]
   return score

def get_top_K(doc_ids,query_tf_idf, tf_idf,TopK=10):
   scores=[]
   results={}
   for doc_id in doc_ids:
      score=get_cos_score(query_tf_idf, tf_idf, doc_id)
      scores.append(score)
      results[str(score)]=doc_id
   scores=heap_sort(scores)
   Temp=min(TopK,len(doc_ids))
   for i  in range(Temp):
      score=scores[i]
      print(str(i+1)+" " + "[%f]"%score+" " + str(results[str(score)])+".html")
      content=get_document_contentent(str(results[str(score)]))
      print(content)

def get_document_contentent(doc_id):
   file_path="./Reuters/"+doc_id+".html"
   with open(file_path,"r") as f:
      lines=f.readlines()
   str = ''
   star=0
   for i in range(len(lines)):
      line=lines[i].strip("\n").split(" ")
      #print(line)
      if len(line)>3:
        if line[2]!='' and line[0]=='':
             str=str+(" ".join(line[2:]))
             star=1
        elif star:
            break
   return str

def topksearch(query,invertedIndex,tf_idf,Topk=10):
    print("词干提取。。。")
    query = lemmatize_sentence(query, True)
    print(query)
    print("纠错。。。")
    inputwords = correctSentence(query)
    print(inputwords)
    query_tf_idf = Cal_query_tf_idf(inputwords, invertedIndex)
    words =set(inputwords)
    if len(words) == 0:
        return []
    docQueue = queue.Queue()
    for word in words:
        docQueue.put(searchOneWord(invertedIndex, word))
    while docQueue.qsize() > 1:
        list1 = docQueue.get()
        list2 = docQueue.get()
        docQueue.put(mergeTwoList(list1, list2))
    doclist = docQueue.get()
    print("从"+str(len(doclist))+"个候选文档中"+"寻找最符合的10个文档!")
    get_top_K(doclist, query_tf_idf, tf_idf)
