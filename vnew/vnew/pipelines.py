# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from vnew.fanyi import translate
import scrapy


class VnewPipelineFanyi(object):
    def __init__(self):
        print('翻译文本内容')

    def process_item(self, item, spider):  # 按段落翻译,分割成句子，然后以字典形式post到翻译接口
        new_paragh = []
        for paragh in item['content']:
            if paragh != ''or '.':
                new_words = translate(paragh)
                new_paragh.append(new_words)

            # 不建议短句翻译，请求太频繁
            if 1 == None:
                new_words = ''
                # 按句子翻译
                words_list = paragh.replace('?', '?.').split('.')
                for words in words_list:
                    if words != '':
                        new_words = translate(words).replace('"', '')
                        if '?' in words:
                            new_words = new_words + '？'
                        # print("---------%s" % new_word)
                new_paragh.append(new_words)
        # if len(item['posted']) != 0:
        #     new_posted = []
        #     for word in item['posted']:
        #         temp = translate(word)
        #         new_posted.append(temp)
        #     item['posted'] = new_posted
        print(new_paragh)
        item['content2'] = new_paragh
        # 文件名不能有特殊字符？/  result = replaceMulti(text, olds, news)
        item['title'] = translate(item['title'].replace('?', '').replace(':', '').replace('/', '')).replace('"', '')
        # 类别只取第一个，没有分类的不改变
        if len(item['posted']) != 0:
            item['posted'] = translate(item['posted'][0].replace('/', '')).replace('"', '')
        # print(item)
        return item


class VnewPipeline(object):
    def __init__(self):
        if not os.path.exists('D:/vnew/'):  # 文件夹不存在则创建
            os.mkdir('D:/vnew/')
    def process_item(self, item, spider):
        # 有部分news没有类别字段
        if len(item['posted']) != 0:
            filedir = item['posted']
        else:
            filedir = 'no_posted'
        print(filedir)
        filename = item['title']
        if not os.path.exists('D:/vnew/' + filedir + '/'):  # 目录不存在则创建
            os.mkdir('D:/vnew/' + filedir + '/')
        if not os.path.exists('D:/vnew/' + filedir + '/' + filename + '.txt'):  # 文章不存在则保存
            with open('D:/vnew/' + filedir + '/' + filename + '.txt', 'w', encoding='utf-8')as f:
                f.write(item['title']+'\n'+item['author']+' '+item['time']+'\n' + '\n'.join(item['content2']))
        return item
