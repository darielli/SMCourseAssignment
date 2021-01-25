import requests
import xlrd
requests.packages.urllib3.disable_warnings()

from lxml import etree
from datetime import datetime, timedelta
from threading import Thread
import csv
from math import ceil
import os
import re
from time import sleep
from random import randint

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': '''your cookie'''
}


def getpage(url):
    res = requests.get(url, headers=headers, verify=False)
    if "跳页" in res.text:
        return res.text
        print("已读取此页")
    else:
        print("获取" + url + "页面时出现问题")
        return 'ERROR'

def parse(page,info, tag):
    result = []
    part = page.split('id="C_')
    num = len(part)
    for i in range(1,num):
        needed, elsepart = part[i].split("</a>", 1)
        id = "C_" + needed.split('">', 1)[0]
        nickname = needed.split('>')[-1]
        content= ''
        elset = ''
        if '<span class="ctt">回复' in elsepart:
            elsepart = elsepart.split('<span class="ctt">回复')[1]
            content, elset = elsepart.split(':', 1)[1].split('<', 1)
        elif '<span class="ctt"><' in elsepart:
            content = ''
            elset = elsepart
        else:
            content, elset = elsepart.split('<span class="ctt">', 1)[1].split('<', 1)
        time = elset.split('<span class="ct">', 1)[1].split('&nbsp')[0]
        if content != '':
            if tag and i == 1:
                result.append([info[0], info[1], info[2], id, nickname, content, time])
            else:
                result.append(['', info[1], '', id, nickname, content, time])
    return  result


def parsefirst(page):
    strtotal = page.split('value="跳页" />&nbsp;')[1].split("页")[0].split("/")[1]
    return int(strtotal)#'4586530633683321">        <a href="/u/5542852741">哈哈哈嘿哈哈呜'


def write_to_csv(result, title, isHeader, pageindex):
    with open(title + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)
        if isHeader == False:
            print('已成功将第{}页{}条评论写入{}中'.format(pageindex, len(result), title + '.csv'))

if __name__ == "__main__":
    filename = "爬评论选中名单.xlsx"
    sheetname = 'Sheet1'
    title = '微博评论数据'
    wb = xlrd.open_workbook(filename=filename)#打开文件
    sheet1 = wb.sheet_by_name('Sheet1')#通过名字获取表格
    sleeptime = 0.5
    #write_to_csv([['微博发布时间', '微博ID', '微博内容', '评论ID', '昵称', '评论内容', '评论发布时间']], title, True, 0)
    for i in range(1, 239):

        wid = sheet1.cell_value(i, 3)
        pubtime = sheet1.cell_value(i, 2)
        content = sheet1.cell_value(i, 5)
        info = [pubtime, wid, content]
        print('即将开始爬取第{}个，wid为{}的微博评论\n\n'.format(i, wid))
        pagenum = 2
        url = "https://weibo.cn/comment/"+wid+"?page=" + str(pagenum)
        page = getpage(url)
        while page == 'ERROR' and pagenum <120:
            pagenum += 1
            url = "https://weibo.cn/comment/" + wid + "?page=" + str(pagenum)
            sleep(sleeptime)
            page = getpage(url)
        if pagenum>=120:
            continue
        total_pagenum = parsefirst(page)
        templist = parse(page, info,True)
        acquireditems = len(templist)
        write_to_csv(templist, title, False, pagenum)
        while acquireditems < 200 and pagenum < total_pagenum:
            pagenum += 1
            url = "https://weibo.cn/comment/" + wid + "?page=" + str(pagenum)
            page = getpage(url)
            if page=='ERROR':
                sleep(sleeptime)
                continue
            templist = parse(page, info, False)
            acquireditems += len(templist)
            write_to_csv(templist, title, False,pagenum)
            sleep(sleeptime)
        print('第{}个，wid为{}的微博评论已爬取完成\n\n'.format(i, wid))