def heap(data,root):
    if 2*root+1<len(data):
        if 2*root+2<len(data) and data[2*root+2]>data[2*root+1]:
            k=2*root+2
        else:
            k=2*root+1
        if data[k]>data[root]:
            data[root],data[k]=data[k],data[root]
            heap(data,k)

def max_heap(data):
    for i in range(len(data)//2-1,-1,-1):
        heap(data,i)
    return data

def heap_sort(data):
    data=max_heap(data)
    li=[]
    for i in range(len(data)-1,-1,-1):
        li.append(data[0])
        if i>0:
            data[0],data[i]=data[i],data[0]
            data=max_heap(data[:i])
    return li
if __name__ == '__main__':
    data=[1,53,6,32,24,8,2,937,43]
    print(heap_sort(data))