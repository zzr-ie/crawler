# -*- coding: utf-8 -*-
import sys

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {

    'Accept':'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Referer':'https://weibo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'SINAGLOBAL=5322006322027.999.1718242561800; SCF=AuwzRszji4YA2E2jL0iQa4HnM1NshJpBQRTXL569Dr4_fUjBL4T5jGtU3kMvkpxW17tartX2Js3v6KEef5s0hY0.; ULV=1741332003110:35:3:3:4945765727147.662.1741332003070:1741164473592; XSRF-TOKEN=xEuJ6YbkmAx_Pl7lhbXK_AOk; ALF=1744458418; SUB=_2A25K1rXiDeRhGeFL71MU9C3MyDmIHXVprbcqrDV8PUJbkNAbLVDgkW1NQg2L8oVmL5FQsBlWXB5UAtX_zW53zIW-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5XX2VMiFN5XjeNTS-Lv98c5JpX5KMhUgL.FoMfSh2fShe7e0-2dJLoIEXLxK-LB-qL12eLxKqL1-eL1h.LxKML1-2L1hBLxK.L1-zLB-2LxKqL1-qLBoet; WBPSESS=X2MXvCU8M26WLReuuHLLPW64yIalGfD3bszs8a8JKKZcw1yoj2RV7VsANkTIFDOXCE617orLVBtPqy9RrHFZec908-w0BBbCnrGrBppF_4k4ow_HEF4Vdm7nnvoF3_3Tbiu4drNLqc4IDk8BVoW4Aw=='
}
CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.JsonWriterPipeline': 100,
    'pipelines.CsvWriterPipeline': 200,
    'pipelines.ImagesDownloadPipeline': 300,
    # 'pipelines.VideoDownloadPipeline': 400,
}
# 图片文件存储路径
IMAGES_STORE = './'
# 视频文件存储路径
FILES_STORE = './'
# 需要的参数
# 模式
modes = ['comment','fan','follow','user','repost','tweet_by_tweet_id','tweet_by_user_id','tweet_by_keyword']
mode = 'tweet_by_keyword'
# 请求字典
KEYWORD_dir = 'keyword_list.txt'
KEYWORD_ids=[]
with open(KEYWORD_dir, 'rb') as f:
    try:
        lines = f.read().splitlines()
        lines = [line.decode('utf-8-sig') for line in lines]
    except UnicodeDecodeError:
        print(u'%s文件应为utf-8编码，请先将文件编码转为utf-8再运行程序', KEYWORD_dir)
    for line in lines:
        if line:
            KEYWORD_ids.append(line)
# 搜索的起始日期，为yyyy-mm-dd-hh形式，搜索结果包含该日期与小时
START_TIME = '2024-10-10-00'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期与小时
END_TIME = '2024-10-14-00'
