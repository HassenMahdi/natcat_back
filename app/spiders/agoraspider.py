
import re

from app.spiders.spider import Spider


class AgoraSpdier(Spider):

    name = "AGORA_SPIDER"
    url = "http://agora.ex.nii.ac.jp"

    def search_by_name(self, name):
        self.driver.get(f'{self.url}/cgi-bin/dt/search_name2.pl?lang=en&name={name}&basin=dontcare')
        return self.driver.find_elements_by_xpath('//tbody/tr/td[2]/a[1]')


    def parse(self, name=None):
        if name:
            links = self.search_by_name(name)
        else:
            return

        hrefs = [l.get_attribute('href') for l in links]
        for h in hrefs:
            for track in self.parse_typhoon_page(h):
                yield track

    def parse_typhoon_page(self, href):
        self.driver.get(href)
        details_href = self.driver.find_element_by_xpath("//a[contains(text(),'Detailed Track Information')]").get_attribute('href')
        self.driver.get(details_href)

        title = self.driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[1]").text
        regex_match = re.search(r'[Typhoon|Cyclone] (?P<code>\d+) \((?P<name>[A-Z]*)\)', title)

        if regex_match:
            code = regex_match.group("code")
            name = regex_match.group("name")
        else:
            code = None
            name = None

        track_info_rows_elem = self.driver.find_elements_by_xpath("//table[@class='TRACKINFO']/tbody/tr")
        for row in track_info_rows_elem[1:]:
            id = row.get_attribute('id')
            is_event = 'event' in row.get_attribute('class')
            row_elements = row.find_elements_by_tag_name('td')
            yield dict(
                id=id,
                is_event=is_event,
                name = name,
                code = code,
                year=row_elements[0].text,
                month = row_elements[1].text,
                day = row_elements[2].text,
                hour = row_elements[3].text,
                lat = row_elements[4].text,
                lon = row_elements[5].text,
                pressure = row_elements[6].text,
                wind = row_elements[7].text,
                classification = row_elements[8].text,
            )

    reports = None
    def pre_process_data(self):
        self.reports = []
    def process_data(self, data):
        self.reports.append(data)


