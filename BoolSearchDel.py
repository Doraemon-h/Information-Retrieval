import nltk
import collections
import re
import queue
from indexcreate import lemmatize_sentence
from spell import correctSentence
import tools
# input is a list of query
# 布尔检索的形式如下  a and b or not c
# 这里规定布尔检索的 not 后不能接bool表达式，只能接查询短语或者查询单词


def searchOneWord(index, word):
    if word not in index:
        return []
    else:
        # 将所有文档id变为数字
        docList = [int(key) for key in index[word].keys()]
        # 将文档的id排序
        docList.sort()
        return docList


def searchPhrase(index, inputList):
    inputList = lemmatize_sentence(inputList,True)
    inputList = correctSentence(inputList)
    words =set(inputList)
    if len(words) == 0:
        return []
    docQueue = queue.Queue()
    for word in words:
        docQueue.put(searchOneWord(index, word))
    while docQueue.qsize() > 1:
        list1 = docQueue.get()
        list2 = docQueue.get()
        docQueue.put(andTwoList(list1, list2))
    doclist = docQueue.get()
    resultList = {}
    if len(inputList) == 1:
        for doc in doclist:
            resultList[doc] = index[inputList[0]][str(doc)]
        return resultList
    # print(doclist)
    for docid in doclist:
        docid = str(docid)
        locList = []
        x = index[inputList[0]][docid]
        for loc in index[inputList[0]][docid]:
            floc = loc
            n = len(inputList)
            hasFind = True
            for word in inputList[1:n]:
                floc += 1
                try:
                    index[word][docid].index(floc)
                except:
                    hasFind = False
                    break
            if hasFind:
                locList.append(loc)
        if len(locList) > 0:
            resultList[docid] = locList
    return resultList


def serarchPhraseForBool(index, wordList,flag):
    if len(wordList) == 0:
        return []
    docQueue = queue.Queue()
    for word in wordList:
        docQueue.put(searchOneWord(index, word))
    while docQueue.qsize() > 1:
        list1 = docQueue.get()
        list2 = docQueue.get()
        docQueue.put(andTwoList(list1, list2))
    doclist = docQueue.get()
    if len(wordList) == 1:
        if flag:
            return doclist
        else:
            return listNotcontain(tools.wholeDocList,doclist)
    reslist = []
    for docid in doclist:
        docid = str(docid)
        locList = []
        x = index[wordList[0]][docid]
        for loc in index[wordList[0]][docid]:
            # print(index[inputList[0]][docid])
            floc = loc
            n = len(wordList)
            hasFind = True
            for word in wordList[1:n]:
                floc += 1
                try:
                    # print(index[word][docid])
                    index[word][docid].index(floc)
                except:
                    hasFind = False
                    break
            if hasFind:
                reslist.append(int(docid))
                break
    if flag:
        return reslist
    else:
        return listNotcontain(tools.wholeDocList,reslist)


def mergeTwoList(list1,list2):
    rlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2 :
        if list1[n1] < list2[n2]:
            rlist.append(list1[n1])
            n1 += 1
        elif list1[n1] > list2[n2]:
            rlist.append(list2[n2])
            n2 += 1
        else:
            rlist.append(list1[n1])
            n1 += 1
            n2 += 1

    if n1 < len1:
        rlist.extend(list1[n1 : len1])
    if n2 < len2:
        rlist.extend(list2[n2 : len2])
    return rlist



def andTwoList(list1,list2):
    rlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            rlist.append(list1[n1])
            n1 += 1
            n2 += 1
    return rlist

#list1中不包含list2的
def listNotcontain(list1,list2):
    rlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            rlist.append(list1[n1])
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            n1 += 1
            n2 += 1
    return rlist

def valueofBoolOp(op):
    precedence = ['OR', 'AND', 'NOT']
    for i in range(3):
        if op == precedence[i]:
            return i
    return -1
#得到后序表达式的栈
def InfxiToPofix(inputList):
    precedence = ['OR','AND','NOT']
    precedence ={}
    precedence['OR'] = 0
    precedence['AND'] = 1
    precedence['NOT'] = 2
    pofix_res = []
    tmp = []
    queries = []
    for word in inputList:
        if(word == '('):
            tmp.append('(')
        elif word == ')':
            if len(queries) > 0:
                pofix_res.append(queries)
                queries = []
            sym = tmp.pop()
            while sym != '(':
                pofix_res.append(sym)
                if len(tmp) == 0:
                    print("Incorrect query")
                    exit(1)  #查询错误退出
                    break
                sym = tmp.pop()
        elif word == 'NOT' or word == "OR" or word == 'AND':
            if len(queries) > 0:
                pofix_res.append(queries)
                queries = []
            if(len(tmp) <= 0):
                tmp.append(word)
            else:
                sym = tmp[len(tmp)-1]
                #弹出到左括号为止
                while len(tmp) >0 and sym != '('and precedence[sym] >= precedence[word]:
                    # pop out
                    pofix_res.append(tmp.pop())
                    if(len(tmp) == 0):
                        break
                    sym = tmp[len(tmp) - 1]
                # push in
                tmp.append(word)
        else:
            # put it into a
            queries.append(word)
            #pofix_res.append(word)
    if len(queries) > 0:
        pofix_res.append(queries)
    while len(tmp) > 0:
        pofix_res.append(tmp.pop())
    return pofix_res


def BoolSearch(query, index):
    print("词干提取。。。")
    query = lemmatize_sentence(query, True)
    print("纠错。。。")
    inputwords = correctSentence(query)
    print(inputwords)
    pofix = InfxiToPofix(query)
    result = []
    nullReturn = []
    limit = len(pofix)
    i = 0
    while i < limit:
        item = pofix[i]
        if item != 'AND'and item !='OR':
            if i < limit - 1:
                if pofix[i+1] == "NOT":
                    i = i + 1
                    result.append(serarchPhraseForBool(index, item, flag=False))
                else:
                    result.append(serarchPhraseForBool(index, item, flag=True))
            else:
                result.append(serarchPhraseForBool(index, item, flag=False))
        elif item == 'AND':
            if len(result) < 2:
                print("illegal query")
                return nullReturn
            else:
                list1 = result.pop()
                list2 = result.pop()
                result.append(andTwoList(list1,list2))
        elif item == 'OR':
            if len(result) < 2:
                print("illegal query")
                return nullReturn
            else:
                list1 = result.pop()
                list2 = result.pop()
                result.append(mergeTwoList(list1,list2))
        i += 1
    if len(result) != 1:
        print("illegal query")
        return nullReturn
    else:
        return result.pop()