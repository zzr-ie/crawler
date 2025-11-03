#!/usr/bin/env python
# encoding: utf-8
"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
import sys

from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_user_info, parse_time, url_to_mid
import settings

class CommentSpider(Spider):
    """
    微博评论数据采集
    """
    name = "comment"

    def start_requests(self):
        """
        爬虫入口
        """
        tweet_ids = settings.KEYWORD_ids

        print(tweet_ids)
        for tweet_id in tweet_ids:
            mid = url_to_mid(tweet_id)
            url = f"https://weibo.com/ajax/statuses/buildComments?" \
                  f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=30"
            yield Request(url, callback=self.parse, meta={'source_url': url, 'mid': tweet_id})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        print(data)
        for comment_info in data['data']:
            item = self.parse_comment(comment_info, response.meta)
            yield item
            # 解析二级评论
            if 'more_info' in comment_info:
                url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={comment_info['id']}" \
                      f"&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id=0&count=100"
                yield Request(url, callback=self.parse, priority=20, meta={'source_url': url, 'mid': response.meta['mid'],'up_comment': item['comment_id']})

        if data.get('max_id', 0) != 0 and 'fetch_level=1' not in response.url:
            url = response.meta['source_url'] + '&max_id=' + str(data['max_id'])
            yield Request(url, callback=self.parse, meta=response.meta)

    @staticmethod
    def parse_comment(data, meta):
        """
        解析comment
        """
        item = dict()
        item['created_at'] = parse_time(data['created_at'])
        item['mid'] = meta['mid']
        item['source_url'] = meta['source_url']
        item['comment_id'] = data['id']
        item['like_counts'] = data['like_counts']
        item['ip_location'] = data.get('source', '')
        item['content'] = data['text_raw']
        comment_user = parse_user_info(data['user'])
        item['comment_user_id'] = comment_user['user_id']
        item['comment_user_avatar_hd'] = comment_user['avatar_hd']
        item['comment_user_nick_name'] = comment_user['nick_name']
        if 'up_comment' in meta:
            item['up_comment'] = meta['up_comment']
        else:
            item['up_comment'] = None
        return item
