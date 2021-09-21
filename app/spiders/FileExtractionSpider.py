import scrapy
from scrapy.crawler import CrawlerProcess

import re
import traceback

from enum import Enum

from app.spiders.spider import Spider


class TitleRegex(Enum):
    #          ------DATE-----  ------DETAILS------- -----------REPORT-----------------
    Basic = r'^(?P<date>[^　]*)　(?P<details>[^\(（]*)(\(|（)(?P<report>[^()（）]*)(\)|）)'
    Date = r'(?P<year>.*)年(?P<month>[0-9]{2})月(?P<day>[0-9]{2})日'
    Details = r'台風第?(?P<number>[0-8]+)'


class ScrapySpider(scrapy.Spider, Spider):
    name = 'FILE_EXTRACTION'

    typhoon_year = None
    typhoon_name = None
    typhoon_code = None

    base_url = 'https://www.fdma.go.jp'

    def start_requests(self):
        return [scrapy.FormRequest(f"{self.base_url}/disaster/info/{self.typhoon_year}/")]

    def parse(self, response: scrapy.http.HtmlResponse, **kwargs):
        documents_list = response.selector.xpath(
            "//body/div[@id='wrapper']/div[4]/div[1]/div[1]/div[1]/ul[1]/li/a[1]"
        )
        doc: scrapy.Selector
        for doc in documents_list:
            try:
                item = {}
                title_str = doc.xpath('./text()').get()
                item["link"] = self.base_url + doc.attrib.get('href')

                # BASIC
                basic_search = re.search(TitleRegex.Basic.value, title_str)
                date_str = basic_search.group('date')
                details_str = basic_search.group('details')
                report_str = basic_search.group('report')
                item['title']=details_str


                # DATE
                date_search=re.search(TitleRegex.Date.value, date_str)
                item["report_year"] = date_search.group('year')
                item["report_month"] = date_search.group('month')
                item["report_day"] = date_search.group('day')

                # Report
                item['report']=report_str

                # Deatils
                details_search = re.search(TitleRegex.Details.value, details_str)
                if details_search:
                    item["number"] = details_search.group('number')
                    item["category"] = 'typhoon'

                print(item)
                yield item

            except Exception as e:
                traceback.print_exc()
                print('UNABLE TO PARSE STRING')


    # Your spider definition
    def execute(self, year, name, code):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(self.__class__, typhoon_year=year, typhoon_name=name, typhoon_code=code)
        process.start()  # the script will block here until the crawling is finished

        print(process)


