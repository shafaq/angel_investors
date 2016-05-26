# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestorItem(scrapy.Item):
    # define the fields for your item here like:
    #name of investor
    name = scrapy.Field()
    #url of the page
    url = scrapy.Field()
    #image url
    image = scrapy.Field()
    #summary
    summary = scrapy.Field()
    #education
    education = scrapy.Field()
    linkedin = scrapy.Field()
    twitter = scrapy.Field()
    facebook = scrapy.Field()
    blog = scrapy.Field()
    website = scrapy.Field()
    followers = scrapy.Field()
    investments = scrapy.Field()
    experience = scrapy.Field()
    what_i_do = scrapy.Field()
    employee = scrapy.Field() #-->
    founder = scrapy.Field() #-->
    advisor = scrapy.Field() #-->
    board_member = scrapy.Field() #-->
    achievements = scrapy.Field()
    skills = scrapy.Field()
    locations = scrapy.Field()
    markets = scrapy.Field()

