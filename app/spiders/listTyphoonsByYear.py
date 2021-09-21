
import re

from app.spiders.spider import Spider


class TyphoonSearchSpider(Spider):

    name = "TYPHOON_LIST__SPIDER"
    url = "http://agora.ex.nii.ac.jp"

    def search_by_name(self, name):
        self.driver.get(f'{self.url}/cgi-bin/dt/search_name2.pl?lang=en&name={name}&basin=dontcare')
        return self.driver.find_elements_by_xpath('//body/div[2]/table[1]/tbody/tr')

    def search_by_year(self, year):
        for basin in ['wsp', 'wnp']:
            uri = f'{self.url}/digital-typhoon/year/{basin}/{year}.html.en'
            self.driver.get(uri)
            for e in self.driver.find_elements_by_xpath('//body/div[2]/table[1]/tbody/tr'):
                yield e


    def parse(self, name=None, year=None, basin='wsp'):
        if name:
            links = self.search_by_name(name)
        elif year:
            links = self.search_by_year(year)
        else:
            return

        for row in links:
            ty = {}
            row_elems = row.find_elements_by_tag_name("td")
            if len(row_elems)>0:
                ty['number'] = row_elems[1].text
                ty['name'] = row_elems[2].text
                ty['basin'] = row_elems[3].text
                ty['birth_date'] = row_elems[4].text
                ty['death_date'] = row_elems[5].text
                ty['duration'] = row_elems[6].text
                ty['min_pressure'] = row_elems[7].text

                yield ty



    reports = None
    def pre_process_data(self):
        self.reports = []
    def process_data(self, data):
        print(data)
        self.reports.append(data)


