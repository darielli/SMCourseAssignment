##用sklearn的PCA

from sklearn.decomposition import PCA
import numpy as np
import csv

sample={1:'好',2: '乐',3:'哀',4:'怒',5:'惧',6:'恶',7:'惊'}
sample2={1:'pos',2:'neg'}

#读取9维心态词典,返回某阶段的无心态数、总数、心态词典
def read(s):
    allResult = {'words': 0, 'sentences': 0, '好': 0, '乐': 0, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
    numOfZero = 0
    count=0
    with open(s, 'r',encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            for r in row:
                # print(r)
                if (r!="" and r[0]=="{"):
                    r=eval(r)
                    y=[]
                    count+=1
                    # print(r)
                    allZero=True
                    for key,val in r.items():
                        if key!="words" and key!="sentences":
                            y.append(val)
                            if val!=0:
                                allZero=False
                        allResult[key]+=val
                    if allZero:
                        numOfZero=numOfZero+1
                    x.append(y)
    return numOfZero,count,allResult
#读取4维心态词典
def read2(s):
    allResult = {'sentences': 0, 'words': 0, 'pos': 0, 'neg': 0}
    numOfZero = 0
    count = 0
    with open(s, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            for r in row:
                # print(r)
                if (r != "" and r[0] == "{"):
                    r = eval(r)
                    y = []
                    count += 1
                    # print(r)
                    allZero = True
                    for key, val in r.items():
                        if key != "words" and key != "sentences":
                            y.append(val)
                            if val != 0:
                                allZero = False
                        allResult[key] += val
                    if allZero:
                        numOfZero = numOfZero + 1
                    x.append(y)
    return numOfZero, count, allResult
#使用sklearn
def pca2(X,k):
    pca = PCA(n_components=k)
    pca.fit(X)
    print(pca.transform(X))
    return
#用numpy进行矩阵运算
def pca1(X,k):
#k is the components you want
    #mean of each feature
    n_samples, n_features = X.shape
    mean=np.array([np.mean(X[:,i]) for i in range(n_features)])
    #normalization
    norm_X=X-mean
    #scatter matrix
    scatter_matrix=np.dot(np.transpose(norm_X),norm_X)
    #Calculate the eigenvectors and eigenvalues
    eig_val, eig_vec = np.linalg.eig(scatter_matrix)
    eig_pairs = [(np.abs(eig_val[i]), eig_vec[:,i]) for i in range(n_features)]
    eig_pairs2 = [(np.abs(eig_val[i]), sample.get(i+1)) for i in range(n_features)]
    # sort eig_vec based on eig_val from highest to lowest
    eig_pairs.sort(reverse=True)
    eig_pairs2.sort(reverse=True)
    for t in eig_pairs2:
        print(t)
    # select the top k eig_vec
    feature=np.array([ele[1] for ele in eig_pairs[:k]])
    #get new data
    data=np.dot(norm_X,np.transpose(feature))
    # print(eig_val)
    print("降维后的数据：")
    print(data)
    return
#把pca1中sample更改为sample2
def pca3(X,k):
    # k is the components you want
    # mean of each feature
    n_samples, n_features = X.shape
    mean = np.array([np.mean(X[:, i]) for i in range(n_features)])
    # normalization
    norm_X = X - mean
    # scatter matrix
    scatter_matrix = np.dot(np.transpose(norm_X), norm_X)
    # Calculate the eigenvectors and eigenvalues
    eig_val, eig_vec = np.linalg.eig(scatter_matrix)
    eig_pairs = [(np.abs(eig_val[i]), eig_vec[:, i]) for i in range(n_features)]
    eig_pairs2 = [(np.abs(eig_val[i]), sample2.get(i + 1)) for i in range(n_features)]
    # sort eig_vec based on eig_val from highest to lowest
    eig_pairs.sort(reverse=True)
    eig_pairs2.sort(reverse=True)
    for t in eig_pairs2:
        print(t)
    # select the top k eig_vec
    feature = np.array([ele[1] for ele in eig_pairs[:k]])
    # get new data
    data = np.dot(norm_X, np.transpose(feature))
    # print(eig_val)
    print("降维后的数据：")
    print(data)
    return
#输出好、乐、哀、怒、惧、恶、惊的心态词典pca结果
def out(s):
    numOfZero, count,allResult = read(s+".csv")
    print(s)
    print("当前时期评论的总的心态字典" + str(allResult))
    print("评论总数量：" + str(count))
    print("无心态情绪评论数量: " + str(numOfZero))
    print("心态字典有效率: " + str(1 - numOfZero / count))
    print("经过PCA处理（按特征值排序）:")
    print(pca1(np.asarray(x), 1))
    # print(pca2(np.asarray(x), 1))
    print("---------------------------------------------------------------")
#输出positive和negative心态词典的pca结果
def out2(s):
    numOfZero, count, allResult = read2(s + ".csv")
    print(s)
    print("当前时期评论的总的心态字典" + str(allResult))
    print("评论总数量：" + str(count))
    print("无心态情绪评论数量: " + str(numOfZero))
    print("心态字典有效率: " + str(1 - numOfZero / count))
    print("经过PCA处理（按特征值排序）:")
    print(pca3(np.asarray(x), 1))
    # print(pca2(np.asarray(x), 1))
    print("---------------------------------------------------------------")



# X = np.array([[-1, 1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# print("测试array： "+str(X))
# print("使用sklearn包得到的结果：")
# pca2(X,1)
# print("使用numpy进行正常矩阵运算的结果：")
# pca1(X,1)
# exit()
# x=[]
# out2("新冠0120-0508正负情感分析（未添加自定义词典）")
x=[]
out("微博评论数据七种心态分析")
# x=[]
# out("正文第二阶段20200123-20200207")
# x=[]
# out("正文第三阶段20200210-20200213")
# x=[]
# out("正文第四阶段20200310-20200630")

# numOfZero,count=read("新冠20191208-20200119八种情感分析.csv")
# print("新冠20191208-20200119")
# print("当前时期评论的总的心态字典"+str(allResult))
# print("评论总数量："+str(count))
# print("无心态情绪评论数量: "+str(numOfZero))
# print("心态字典有效率: "+str(1-numOfZero/count))
# print("经过PCA处理（按特征值排序）:")
# print(pca1(np.asarray(x),1))
# print(pca2(np.asarray(x),1))
# print("---------------------------------------------------------------")
# numOfZero,count=read("新冠0120-0508八种情感分析.csv")
# print("新冠20200120-20200508")
# print("当前时期评论的总的心态字典"+str(allResult))
# print("评论总数量："+str(count))
# print("无心态情绪评论数量: "+str(numOfZero))
# print("心态字典有效率: "+str(1-numOfZero/count))
# print("经过PCA处理（按特征值排序）:")
# print(pca1(np.asarray(x),1))
# print(pca2(np.asarray(x),1))
# print("---------------------------------------------------------------")
# numOfZero,count=read("新冠0509-0630八种情感分析.csv")
# print("新冠20200509-20200630")
# print("当前时期评论的总的心态字典"+str(allResult))
# print("评论总数量："+str(count))
# print("无心态情绪评论数量: "+str(numOfZero))
# print("心态字典有效率: "+str(1-numOfZero/count))
# print("经过PCA处理（按特征值排序）:")
# print(pca1(np.asarray(x),1))
# print(pca2(np.asarray(x),1))


# print(383729/45)
# print(18579/45)
# print()
# print(348537/15)
# print(17574/15)
# print()
# print(114381/3)
# print(5185/3)
# print()
# print(3683657/115)
# print(169970/115)




