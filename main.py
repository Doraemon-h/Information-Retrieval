from BoolSearchDel import BoolSearch,searchPhrase
from getIndex import getIndex
from topk import topksearch


print("getting word list...")
invertedIndex = getIndex("./dictionary/invertedIndex.json")
print("getting index...")
wordlist = getIndex("./dictionary/wordList.json")
print("getting tf-idf...")
tf_idf = getIndex("./dictionary/nomalized_tf_idf.json")

while(1):
    print("搜索操作: ")
    print("[1] TOP K [2]布尔查询 [3]短语查询（布尔） [4]exit")
    print("请输入你选择的序号：")
    try:
        choice = int(input())
        if choice == 4:
            break
    except :
        print()
        continue
    if choice >= 1 and choice <= 3:
        print("请输入查询语句")
        s = input()
        if s == "EXIT":
            break
        #查询排序
        if choice == 1:
            topksearch(s,invertedIndex,tf_idf,Topk=10)
        #TOP K 查询
        elif choice == 2:
            doc=BoolSearch(s,invertedIndex)
            print(len(doc),"DOCs :")
            print(doc)
        elif choice ==3:
            phrasedoc = searchPhrase(invertedIndex, s)
            if 0 == len(phrasedoc):
                print("Doesn't find \"", s, '"')
            else:
                for key in phrasedoc:
                    print('docID: ', key, "   num: ", len(phrasedoc[key]))
                    print('    location: ', phrasedoc[key])
    else:
        print("输入格式错误，请重新输入！！！")
    print()
