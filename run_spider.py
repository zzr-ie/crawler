#!/usr/bin/env python
# encoding: utf-8
import sys
print(sys.path)
import dateutil.parser


"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2019-12-07 21:27
"""
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tweet_by_user_id import TweetSpiderByUserID
from spiders.tweet_by_keyword import TweetSpiderByKeyword
from spiders.tweet_by_tweet_id import TweetSpiderByTweetID
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.user import UserSpider
from spiders.fan import FanSpider
from spiders.repost import RepostSpider
import settings
if __name__ == '__main__':
    mode = settings.mode
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'comment': CommentSpider,# 微博评论数据采集
        'fan': FanSpider,# 微博粉丝数据采集
        'follow': FollowerSpider, # 微博关注数据采集
        'user': UserSpider, # 微博用户信息爬虫
        'repost': RepostSpider, # 微博转发数据采集
        'tweet_by_tweet_id': TweetSpiderByTweetID,# 用户推文ID采集推文
        'tweet_by_user_id': TweetSpiderByUserID, # 用户推文数据采集
        'tweet_by_keyword': TweetSpiderByKeyword, #关键词搜索采集
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
