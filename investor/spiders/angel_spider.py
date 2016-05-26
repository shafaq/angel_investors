import scrapy
from investor.items import InvestorItem
from investor.investorloader import InvestorLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException



class AngelSpider(scrapy.Spider):
    name = "angel"
    allowed_domains = ["angel.co"]
    filename = 'URL.csv'
    #start_urls = ['https://angel.co/csc-upshot']
    #start_urls = ['file:///home/shafaq/projects/investor/AlexMashinsky.html',]
    def start_requests(self):

        url = 'https://angel.co/armando-biondi'
        yield scrapy.Request(url, self.parse, meta={
            'splash': {
            'args': {
            'wait' : 10.0,
            },
            'endpoint': 'render.html',
          }
          })





    def parse(self, response):

        l = InvestorLoader(item=InvestorItem(), response=response)
        l.add_xpath('name', '//body//div[@class="js-header-complete"]\
                    //h1[contains(concat(" ", normalize-space(@class)," "), " js-name ")]/text()', TakeFirst(), unicode.strip)
        l.add_value('url',response.url)
        l.add_xpath('image', '//body//div[contains(@class,"js-header-complete")]//img[contains(@class,"js-avatar-img")]/@src', TakeFirst(), response.urljoin)
        l.add_xpath('summary', '//div[@class="s-grid0-colSm24"]//p//text()')

        l.add_css('linkedin' , 'div.js-header-complete div.u-inlineBlock.u-blockSmOnly span>a[data-field="linkedin_url"]::attr(href)',
                    TakeFirst(), unicode.strip)
        l.add_css('facebook', 'div.js-header-complete div.u-inlineBlock.u-blockSmOnly span>a[data-field="facebook_url"]::attr(href)',
            TakeFirst(), unicode.strip)
        l.add_css('twitter', 'div.js-header-complete div.u-inlineBlock.u-blockSmOnly span>a[data-field="twitter_url"]::attr(href)',
                    TakeFirst(), unicode.strip)
        l.add_css('blog', 'div.js-header-complete div.u-inlineBlock.u-blockSmOnly span>a[data-field="blog_url"]::attr(href)',
                TakeFirst(), unicode.strip)
        l.add_css('website', 'div.js-header-complete div.u-inlineBlock.u-blockSmOnly span>a[data-field="online_bio_url"]::attr(href)'
            ,TakeFirst(), unicode.strip)
        l.add_css('followers', 'div.content div.social a.following_count::text', TakeFirst(), re='([\d,]+) Following')
        '''l.add_xpath('investments', '//div[contains(@class,"js-investments")]//div[contains(@class,"investment")]\
                       //div[contains(@class,"company-link")]/a/text()')
        '''
        l.add_css('education', 'div.js-header-complete div.tags>span:last-of-type>a::text', TakeFirst(), unicode.strip)

        experience = ''

        exp_sel = response.xpath('//div[contains(concat(" ",normalize-space(@class)," "), " experience ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," two_col_block ")]\
            //div[not(contains(concat(" ",normalize-space(@class)," "), " hidden "))]')
        for sel in exp_sel:
            #experience = ''
            #role = sel.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," left_block ")]/text()').extract_first()
            role = ''
            e = ''
            role = sel.xpath('./@data-role').extract_first()
            e = ''.join(sel.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," right_block ")]//text()').extract())
            if role and e:
                role = role.strip().lower()
                experience += role + ":" + e
                #print "role = " + role
                #print "experience = " + experience
                if role in ['founder', 'employee', 'advisor', 'board_member']:
                    l.add_value(role, e)




        l.add_value('experience', experience)
        l.add_xpath('what_i_do', '//div[contains(concat(" ",normalize-space(@class)," "), " about ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," content ")]\
            //div[contains(concat(" ",normalize-space(@class)," "), " summary ")]//p//text()')
        l.add_xpath('achievements', '//div[contains(concat(" ",normalize-space(@class)," "), " about ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," content ")]\
            //div[contains(concat(" ",normalize-space(@class)," "), " what_ive_built ")]//p//text()')

        l.add_xpath('skills', '//div[contains(concat(" ",normalize-space(@class)," "), " about ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," content ")]\
            //div[contains(@data-field, "tags_skills")]//a/text()')

        l.add_xpath('locations', '//div[contains(concat(" ",normalize-space(@class)," "), " about ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," content ")]\
            //div[contains(@data-field,"tags_interested_locations")]//a/text()')

        l.add_xpath('markets', '//div[contains(concat(" ",normalize-space(@class)," "), " about ")]\
            //div[contains(concat(" ",normalize-space(@class)," ")," content ")]\
            //div[contains(@data-field,"tags_interested_markets")]//a/text()')

        #for investments
        '''driver = webdriver.Firefox()
        driver.get(response.url)
        try:
            element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"js-investments")]//div[contains(@class,"investment")]\
                       //div[contains(@class,"company-link")]/a')))

        except TimeoutException:
            print "******Timeout"
          #log
        else:
            print "*******Fine"
            try:
                more = driver.find_element_by_xpath('//div[contains(@class,"js-investments")]//div[contains(@class,"investment")]\
                       //div[contains(@class,"more_button")]')
                print "******more not found"
                more.click()
            except NoSuchElementException:
                print "*****more not found"
                pass
                #log

            finally:

                investment_list =  driver.find_elements_by_xpath('//div[contains(@class,"js-investments")]//div[contains(@class,"investment")]\
                       //div[contains(@class,"company-link")]/a')
                l.add_value('investments', ', '.join([x.text for x in investment_list]))
            #print investment_list
        finally:
            driver.quit()
        '''
        investment_list =  map(unicode.strip,response.xpath('//div[contains(@class,"js-investments")]//div[contains(@class,"investment")]\
                       //div[contains(@class,"company-link")]/a/text()').extract())
        l.add_value('investments', u', '.join(investment_list))

        yield l.load_item()


