import os
import xlsxwriter
import time

def trans(path):
    keyword_list = ['医疗队', '新冠', '病毒', '肺炎', '疾控', '口罩', '疫情', '防护服', '火神山', '雷神山',
                    '防疫', '确诊', '抗疫', '逆行', '医务人员', '感染', '病例', '卫健委', '志愿者', '消毒', '隔离', '核酸检测']
    with open(path, encoding='utf-8') as f:
        line = f.readlines()
    nickname = line[1].split('：')[1]
    user_id = line[2].split('：')[1]
    year, start_time, end_time = path.split("/")[1].split(".") [0].split(" ")
    chart_title = nickname.strip()+'微博内容'
    c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    xls2 = xlsxwriter.Workbook(chart_title + " " + year+start_time+'-'+year+end_time+ '.xlsx')
    sht1 = xls2.add_worksheet(start_time+'-'+end_time)

    sht1.write(0, 0, nickname + year + '年' + start_time +'至' + end_time + '微博')
    sht1.write(1, 0, "创建时间:")
    sht1.write(1, 1, c_time)
    sht1.write(2, 0, '微博总条数')
    #最后需要写如总条数
    sht1.write(3, 0, '用户ID')
    sht1.write(3, 1, user_id)
    sht1.write(4, 0, '用户昵称')
    sht1.write(4, 1, nickname)

    sht1.write(6, 0, '序号')
    sht1.write(6, 1, '微博创建时间')
    sht1.write(6, 2, '微博ID')
    sht1.write(6, 3, '微博MID')
    sht1.write(6, 4, '微博信息内容')
    sht1.write(6, 5, '微博转发数')
    sht1.write(6, 6, '微博评论数')
    sht1.write(6, 7, '微博点赞数')
    retweet_count = 0
    comment_count = 0
    up_count = 0
    index = 1
    total_counts = int((len(line)-8)/7)
    for i in range(1, total_counts+1):
         if any(name in line[7*i+1] for name in keyword_list):
            sht1.write(index+6, 0, i)
            sht1.write(index+6, 1, line[7*i+3].split("：")[1].strip())
            sht1.write(index+6, 2, line[7*i+2].split("：")[1].strip())
            sht1.write(index+6, 4, line[7*i+1].strip())
            sht1.write(index+6, 5, int(line[7*i+5].split("：")[1].strip()))
            retweet_count += int(line[7 * i + 5].split("：")[1].strip())
            sht1.write(index+6, 6, int(line[7*i+6].split("：")[1].strip()))
            comment_count += int(line[7 * i + 6].split("：")[1].strip())
            sht1.write(index+6, 7, int(line[7*i+4].split("：")[1].strip()))
            up_count += int(line[7 * i + 4].split("：")[1].strip())

            index += 1
         else:
             continue

    sht1.write(2, 1, index-1)
    xls2.close()

    return [index-1, retweet_count, comment_count, up_count]

if __name__ == '__main__':
    # path = 'textData/2020 0621 0630.txt'
    # trans(path)
    path_list = os.listdir('textData')
    weibo_count = 0
    retweet_count = 0
    comment_count = 0
    up_count = 0
    for path in path_list:
        temp1, temp2, temp3, temp4  = trans('textData/'+path)
        weibo_count += temp1
        retweet_count += temp2
        comment_count += temp3
        up_count += temp4

    print([weibo_count, retweet_count, comment_count, up_count])
    #未删减    [11134,     93683990,     34809466,   525997352]
    #疫情相关   [6672,     55759005,     21329516,   348042329]
    #           1.66       1.68            1.63      1.511