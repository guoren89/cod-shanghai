import scrapy

from cod import settings
from cod.items import CodItem


class Cod19Spider(scrapy.Spider):
    name = 'cod19'
    # allowed_domains = ['https://ss.shanghai.gov.cn/search?page=1&view=&contentScope=2&dateOrder=2&tr=1&dr=&format=1&uid=aeb40557-eb1f-5566-6a5a-dafb05907869&sid=0000016f-12d7-2c3c-28c0-49855413294d&re=2&all=1&debug=&siteId=wsjkw.sh.gov.cn&siteArea=all&q=%EF%BC%8C%E4%B8%8A%E6%B5%B7%E6%96%B0%E5%A2%9E%E6%9C%AC%E5%9C%9F%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E']
    # start_urls = ['https://wsjkw.sh.gov.cn/yqtb/index.html']
    start_urls = []

    def __init__(self):
        start_page = settings.start_page
        end_page = settings.end_page
        for i in range(start_page, end_page + 1):
            if i == 1:
                url = 'https://wsjkw.sh.gov.cn/yqtb/index.html'
                Cod19Spider.start_urls.append(url)
            else:
                url = f'https://wsjkw.sh.gov.cn/yqtb/index_{i}.html'
                Cod19Spider.start_urls.append(url)

    def parse(self, response):
        news = response.xpath('//ul[@class="uli16 nowrapli list-date "]/li')
        print(len(news))
        for b in news:
            title = b.xpath('.//a/text()').extract_first()
            print(title)
            item = CodItem()
            item['title'] = title
            yield item

        pass
