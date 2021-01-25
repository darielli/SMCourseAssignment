def count(path):
    with open(path, encoding='utf-8') as f:
        weibo_num = 0
        retweet_num = 0
        comment_num = 0
        up_num = 0
        line = f.readlines()
        #先看用户信息
        #然后再看微博内容
        for content in line:
            if content.startswith('评论数：'):
                temp = int(content.split('：')[1])
                comment_num += temp
            if content.startswith('点赞数：'):
                temp = int(content.split('：')[1])
                up_num += temp
            if content.startswith('转发数：'):
                temp = int(content.split('：')[1])
                retweet_num += temp
                weibo_num += 1
    return [weibo_num, comment_num, up_num, retweet_num]







if __name__ =='__main__':
    path = 'textData/2020 0201 0210.txt'
    weibo_num, comment_num, up_num, retweet_num = count(path)
