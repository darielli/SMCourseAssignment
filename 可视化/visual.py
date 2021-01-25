import numpy as np
import matplotlib.pyplot as plt
import csv
import xlwt
import pandas as pd


def export_excel(export):
   #将字典列表转换为DataFrame
   pf = pd.DataFrame(list(export))
   #指定字段顺序
   # order = ['日期','好', '乐', '哀', '怒', '惧', '恶', '惊']
   order = ['日期','pos','neg']

   pf = pf[order]
   #将列名替换
   # columns_map = {
   #    '日期':'日期',
   #    '好':'好',
   #    '乐':'乐',
   #    '哀':'哀',
   #    '怒':'怒',
   #    '惧':'惧'
   # }
   columns_map = {
       '日期': '日期',
       'pos': 'pos',
       'neg': 'neg'
   }
   pf.rename(columns = columns_map,inplace = True)
   #指定生成的Excel表格名称
   # file_path = pd.ExcelWriter('评论七种心态每日变化.xlsx')
   file_path = pd.ExcelWriter('正文正负心态每日变化.xlsx')
   #替换空单元格
   pf.fillna(' ',inplace = True)
   #输出
   pf.to_excel(file_path,encoding = 'utf-8',index = False)
   #保存表格
   file_path.save()
# if __name__ == '__main__':
#     #将分析完成的列表导出为excel表格
#     table=[]
#
#     export_excel({"日期":0,'好': 0, '乐': 0, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0})

def makeVisual(allResult):
    # 用于正常显示中文
    plt.rcParams['font.sans-serif'] = 'SimHei'
    # 用于正常显示符号
    plt.rcParams['axes.unicode_minus'] = False
    # 使用ggplot的绘图风格
    plt.style.use('ggplot')
    # 构造数据
    values = [0,0,0,0,0,0,0]
    i=1
    for key,val in allResult.items():
        if key!="sentences" or key!='words':
            values[i]=val
            i+=1
            if i==7:
                i=0
    feature = ['nothing', '好', '乐', '哀', '怒', '惧', '恶', '惊']
    # 设置每个数据点的显示位置，在雷达图上用角度表示
    angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False)
    # 拼接数据首尾，使图形中线条封闭
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    # 绘图
    fig = plt.figure()
    # 设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'o-', linewidth=2)
    # 填充颜色
    ax.fill(angles, values, alpha=0.25)
    # 设置图标上的角度划分刻度，为每个数据点处添加标签
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    # 设置雷达图的范围
    ax.set_ylim(0, 200)
    # 添加标题
    plt.title('新冠每日心态词典变化雷达图')
    # 添加网格线
    ax.grid(True)

    plt.show()


def changeTheDate(date):
    d=date.split("-")
    d[2]=int(d[2])+1
    d[1]=int(d[1])+0
    d[0]=int(d[0])+0
    if d[2]==30:
        if d[1]==2:
            d[1]+=1
            d[2]=1
    if d[2]==32:
        d[1]+=1
        d[2]=1
    if d[2]==31:
        if (d[1]==4) or (d[1]==6):
            d[1]+=1
            d[2]=1
    if d[1]==13:
        d[0]+=1
        d[1]=1
    if d[1]<10:
        d[1]="0"+str(d[1])
    if d[2]<10:
        d[2]="0"+str(d[2])
    return str(d[0])+"/"+str(d[1])+"/"+str(d[2])

def read(s,x):
    numOfZero = 0
    count = 0
    oneDay = True
    date = "2019-12-31"
    table=[]
    # out={'日期':"0", '好': 0, '乐': 0, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
    out = {'日期': "0", 'pos':0,'neg':0}
    # allResult={'words': 0, 'sentences': 0, '好': 0, '乐': 0, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
    allResult = {'words': 0, 'sentences': 0, 'pos':0,'neg':0}

    with open(s+".csv", 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            for r in row:
                if r[0:5]=="2019-"or r[0:5]=="2020-" :
                    i=0
                    oneDay=True
                    while r[i]!=" ":
                        if (r[i]!=date[i]):
                            oneDay=False
                            break
                        i+=1
                    if (oneDay==False):
                        # makeVisual(allResult)
                        date=changeTheDate(date)
                        out["日期"]=date
                        for k,v in allResult.items():
                            if k != "words" and k != "sentences":
                                out[k]=v
                        print(out)
                        table.append(out.copy())
                        # print(table)
                        # allResult={'words': 0, 'sentences': 0, '好': 0, '乐': 0, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
                        allResult = {'words': 0, 'sentences': 0, 'pos':0,'neg':0}

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
    export_excel(table)
    return numOfZero, count, allResult,x


read("微博正文数据正负心态分析",[])