import scrapy
from scrapy.http import HtmlResponse
import getpass
from parse_gb.items import ParseGbItem
from scrapy.loader import ItemLoader


class GbSpider(scrapy.Spider):
    name = 'gb'
    allowed_domains = ['gb.ru']
    start_urls = ['https://gb.ru']
    login_link = 'https://ctm.gb.ru/mtc/event'  # 'https://gb.ru/login'
    programm_link = 'courses/all'
    login_gb = getpass.getpass('Введите логин: ')
    pwd_gb = getpass.getpass('Введите пароль: ')

    def parse(self, response: HtmlResponse, **kwargs):

        csrf = 'qPixbFnV007aIm9ppbFvfk2n13nFdmcxIQLYdt+dJu+68vsPJNSWSgeEjt4xuTPlhQgu0HWO91P+J0PusjLQDw=='

        yield scrapy.FormRequest(
            self.login_link,
            method='POST',
            callback=self.login,
            formdata={'user_email': self.login_gb, 'user_password': self.pwd_gb},
            headers={'csrf-token': csrf}
        )

    def login(self, response: HtmlResponse):

        j_body = response.json()
        if j_body['success'] == 1:
            yield response.follow(
                f'https://gb.ru/{self.programm_link}',
                callback=self.parse_data,
                cb_kwargs={'programm': self.programm_link}
            )

    def parse_data(self, response: HtmlResponse, **kwargs):

        links = response.xpath('//div[@class="ui-col-xl-9"]//a[@class="card_full_link"]')

        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse, **kwargs):

        loader = ItemLoader(item=ParseGbItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('level', "//div[@data-cpid='gbc-d9316bb9-d53d-4cf3-ad64-2b6f37742c4e']//div[@class='gkb-label-card__label-right']/span[2]/text()")
        loader.add_xpath('learning_lines',
                         '//p[@class="gkb-promo__text-secondary ui-text-body--5"]/text()')
        loader.add_xpath('price_per_month', '//div[@data-cpid="gbc-d9316bb9-d53d-4cf3-ad64-2b6f37742c4e"]//div[@class = "gkb-promo__price-current"]/span[@data-price="price_main"]/text()')
        loader.add_value('url', response.url)
        yield loader.load_item()


