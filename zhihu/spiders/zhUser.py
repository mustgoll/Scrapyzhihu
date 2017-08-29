# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from zhihu.items import UserItem
class ZhuserSpider(scrapy.Spider):
    name = 'zhUser'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    start_user='sprachel'
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    follower_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follower_include='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield  Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield  Request(self.follower_url.format(user=self.start_user,include=self.follower_include,offset=0,limit=20),callback=self.parse_follower)
    def parse_user(self, response):
        result=json.loads(response.text)
        item=UserItem()
        for i in item.fields:
            if i in result.keys():
                item[i]=result[i]
        yield item
        yield Request(self.follower_url.format(user=item['url_token'],include=self.follower_include,offset=0,limit=20),callback=self.parse_follower)

    def parse_follower(self, response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in results.keys() and results['paging']['is_end']==False:
            next_page=results['paging']['next']
            yield Request(next_page,callback=self.parse_follower)
