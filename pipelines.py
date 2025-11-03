# -*- coding: utf-8 -*-
import copy
import csv
import datetime
import json
import os.path
import time

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

import settings

class JsonWriterPipeline(object):
    """
    写入json文件的pipline
    """

    def __init__(self):
        self.file = None
        if not os.path.exists('../output'):
            os.mkdir('../output')

    def process_item(self, item, spider):
        """
        处理item
        """
        if not self.file:
            now = datetime.datetime.now()
            file_name = spider.name + "_" + now.strftime("%Y%m%d%H%M%S") + '.jsonl'
            self.file = open(f'../output/{file_name}', 'wt', encoding='utf-8')
        item['crawl_time'] = int(time.time())
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item

class CsvWriterPipeline(object):

    def __init__(self):
        self.table_header_file = 'table_header.json'
        self.table_headers = None
        self.file = None
        self.base_dir = 'results'+ os.sep + settings.mode+ os.sep + 'csvresults'
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def open_spider(self, spider):
        # 表头信息
        with open(self.table_header_file, 'r', encoding='utf-8-sig') as f:
            table_header_dicts = json.load(f)
        for load_dict in table_header_dicts:
            if load_dict['mode'] == settings.mode:
                self.table_headers = load_dict["table_header"]
        # 新建文件
        if not self.file:
            now = datetime.datetime.now()
            file_name = settings.mode + "_" + now.strftime("%Y%m%d%H%M%S") + '.csv'
            self.csvfile = open(f"{self.base_dir}/{file_name}", 'wt', encoding='utf-8-sig',
                                newline='')
        self.csvwriter = csv.writer(self.csvfile)
        self.csvwriter.writerow(self.table_headers.keys())
        self.csvfile.flush()

    def process_item(self, item, spider):
        item['crawl_time'] = int(time.time())
        self.csvwriter.writerow([item[key] for key in self.table_headers.keys()])
        self.csvfile.flush()
        return item


class ImagesDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if len(item['pic_urls']) == 1:
            yield scrapy.Request(item['pic_urls'][0],
                                 meta={
                                     'item': item,
                                     'sign': ''
                                 })
        elif len(item['pic_urls']) > 1:
            sign = 0
            for image_url in item['pic_urls']:
                yield scrapy.Request(image_url,
                                     meta={
                                         'item': item,
                                         'sign': '-' + str(sign)
                                     })
                sign += 1

    def file_path(self, request, response=None, info=None):
        image_url = request.url
        item = request.meta['item']
        sign = request.meta['sign']
        base_dir = 'results'+ os.sep + settings.mode+ os.sep + 'images'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        image_suffix = image_url[image_url.rfind('.'):]
        file_path = base_dir + os.sep + item['_id'] + sign + image_suffix
        return file_path


class VideoDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['video']:
            yield scrapy.Request(item['video'],
                                 meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        base_dir = 'results'+ os.sep + settings.mode+ os.sep + 'videos'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['_id'] + '.mp4'
        return file_path
