import scrapy
from mental_health.items import MentalHealthItem
from scrapy.selector import Selector
import requests
import re
import urllib.request
from urllib.parse import urlparse
from w3lib.html import  remove_tags
import unicodedata
import datetime
from urllib.parse import urljoin
from mental_health import settings
import logging
from w3lib.http import basic_auth_header
from scrapy import signals
from pydispatch import dispatcher
from scrapy.http import FormRequest
from lxml.html import fromstring
from bs4 import BeautifulSoup

#//*[@id="ba-content"]//tbody//td[2]/a/@href

class scraper(scrapy.Spider):
    name="mental_health_2"
    allowed_domains = ["healthunlocked.com"]
    
    PROJECT_ROOT=settings.PROJECT_ROOT

    def start_requests(self):
    
        # urls=['https://healthunlocked.com/healmyptsd/posts/149835982/dissociative-seizures-from-ptsd','https://healthunlocked.com/anxiety-depression-support/posts/149827453/intrusive-thoughts-of-ex']
        urls=[]
        pages= range(1,100)
        for i in pages:
            urls.append('https://healthunlocked.com/tag/bipolar%20disorder?page={}&community=all'.format(i))
            urls.append('https://healthunlocked.com/tag/obsessive%20compulsive%20disorder%20ocd?page={}&community=all'.format(i))
            urls.append('https://healthunlocked.com/tag/anxiety?page={}&community=all'.format(i))
            urls.append('https://healthunlocked.com/tag/clinical%20depression?page={}&community=all'.format(i))
            urls.append('https://healthunlocked.com/tag/post%20traumatic%20stress%20disorder%20ptsd?page={}&community=all'.format(i))
        
        for i in urls:
            yield scrapy.Request(i, callback=self.links)
    
    def links(self,response):
        lin=[]
        hxs = Selector(response)
        self.tag=hxs.xpath('//a[@class="active"]/@href').extract()[0].replace('/tag/','')
        hrefs= hxs.xpath('//div[@class="results-posts"]//a//h3//parent::*/@href').extract()
        for i in hrefs:
            yield scrapy.Request(urljoin('https://healthunlocked.com',i), callback=self.parse)


    def parse(self, response):
        hxs = Selector(response)
        
        header= hxs.xpath('//h1[@id="post-heading"]//text()').extract()[0]
        prob=hxs.xpath('//div[@class="post-body"]//text()').extract()
        for quote in hxs.xpath('//div[@class="sc-d94c948d-0 grqulI"]'):
            bodies = BeautifulSoup(' '.join(quote.xpath('./p/text()').extract()))
            bodies = bodies.get_text().strip()
            # title= quote.xpath('.//h3/text()')[0].extract()
            # user= quote.xpath('.//a[contains(@href,"/user")]/text()').extract()
            item= MentalHealthItem()
            item["title"]=header
            item['tag']=self.tag
            item['Concern']=prob
            item["Suggestion"]=bodies
            
            yield item
            