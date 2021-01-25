import pandas as pd
import 情感分析

data = pd.read_csv(r'微博评论数据.csv')
#print(data.columns)#获取列索引值
data1 = data['微博全文']#获取列名为flow的数据作为新列的数据
temp=[]
for d in data1:
    temp.append(str(情感分析.emotion(str(d))))
data['正负情感分析']=temp
data.to_csv(r"微博评论数据七种心态分析.csv",index =False)
#mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
#print(temp)