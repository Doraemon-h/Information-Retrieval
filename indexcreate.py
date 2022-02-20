import os
import tools
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
import json

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

deleteSignal = [',','.',';','&',':','>',"'",'`','(',')','+','!','*','"','?']
deleteSignalForInput = [',','.',';','&',':','>',"'",'`','+','!','*','"','?']

def getWord(word):
    if word.istitle():
        word = word.lower()
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    else:
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    return word

def lemmatize_sentence(sentence,forinput):
    res = []
    result = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    for word in res:
        #如果是 's什么的，直接排除,排除空的字符串
        if word[0] is '\'' or len(word) is 0 or word[0] is '-':
            continue
        #去除标点符号
        if not forinput:
            for c in deleteSignal:
                word = word.replace(c,'')
        else:
            for c in deleteSignalForInput:
                word = word.replace(c,'')
        #如果分解的单词中有/,则将其中的每个单词添加到结果中
        if word.find('/') > 0:
            rs = word.split('/')
            for w in rs:
                w = getWord(w)
                result.append(w)
        else:
            word = getWord(word)
            result.append(word)
    return result


def preProcess(filename):
    file = open(filename,'r')
    content = file.read()
    words = lemmatize_sentence(content,False)
    return words

def processDirectory(directname):
    path = tools.projectpath
    path += directname
    files = os.listdir(path)
    result = []
    for file in files:
        content = preProcess(path + '/' + file)
        result.append(content)
        # print(content)
    return result


#获取文档名中的文档的id
def getDocID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)

def printIndex(index):
    for stem in index:
        print(stem)
        for doc in index[stem]:
            print("    " , doc , " : " , index[stem][doc])

def getWordList(invertedIndex):
    wordList = []
    for word in invertedIndex.keys():
        wordList.append(word)
    return wordList

def createIndex(directname):
    invertedIndex = {}
    path = "./" + directname
    files = os.listdir(path)
    for file in files:
        print("analyzing file: ", file)
        #每个文档的词项 list
        content = preProcess(path + '/' + file)
        docId = getDocID(file)

        num = 0 #word在文档中的位置
        for word in content:
            if word not in invertedIndex:
                docList = {}
                docList[docId] = [num]
                invertedIndex[word] = docList
            else:
                if docId not in invertedIndex[word]:
                    invertedIndex[word][docId] = [num]
                else:
                    invertedIndex[word][docId].append(num)
            num += 1
    #获取词项列表
    wordList = getWordList(invertedIndex)
    print("1")
    # printIndex(invertedIndex)
    with open("./dictionary/invertedIndex.json","w") as f:
        json.dump(invertedIndex,f)
    with open("./dictionary/wordList.json","w") as f:
        json.dump(wordList,f)        
        
      

if __name__=="__main__":
    createIndex("Reuters")