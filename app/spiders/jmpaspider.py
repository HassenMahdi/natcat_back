import time

from app.spiders.spider import Spider


class JMASpiderXPaths:
    typhoon_details_table = "//body/div[@id='unitmap-switches']/div[@id='unitmap-selector']/div[@id='unitmap-textinfo']/div[1]/div[1]/table[1]/tr"
    nav_menu_item = "//a[@id='label_elem']"
    typhoon_list = "/html[1]/body[1]/div[4]/nav[1]/div[3]/div[2]/ul[1]/li[1]/div[1]/ul[1]/li[1]/ul[1]/li/a"
    map = "//div[@id='unitmap']"
    # map = "//body/div[@id='unitmap']/div[1]/div[11]/canvas[1]"

xpaths = JMASpiderXPaths()

class JMASpdier(Spider):
    name = "JMA_SPIDER"

    observation_driver = None

    def wait_for_map(self):
        # WORKAROUND
        time.sleep(10)

    def get_typhoon_nav_elements(self):
        return self.driver.find_elements_by_xpath(xpaths.typhoon_list)[1:]

    def typhoon_screenshot(self):
        return self.driver.find_element_by_xpath(xpaths.map).screenshot_as_base64

    def parse(self):
        self.driver.get("https://www.jma.go.jp/bosai/map.html#contents=typhoon&lang=en")
        self.wait_for_map()

        typhoon_count = len(self.get_typhoon_nav_elements())

        for typhoon_index in range(0, typhoon_count):
            nav_menu_item_elem = self.driver.find_element_by_xpath(xpaths.nav_menu_item)
            nav_menu_item_elem.click()
            typhoon_elem = self.get_typhoon_nav_elements()[typhoon_index]
            typhoon_elem.click()
            description_table_rows_elem = self.driver.find_elements_by_xpath(xpaths.typhoon_details_table)

            # EXTRACT ANALYSIS SECTIONS
            title = description_table_rows_elem[0].text
            issue_date = description_table_rows_elem[1].text
            base64_screenshot = self.typhoon_screenshot()
            # print(base64_screenshot)

            section = None
            for row in description_table_rows_elem[2:]:
                row_class = row.get_attribute("class")
                if row_class == "contents-header":
                    if section:
                        yield section
                    section = {
                        "Typhoon Code(Name)": title,
                        "Issue Date": issue_date,
                        "Issue/Forcast Date":row.text,
                        "base_64_image":base64_screenshot
                    }
                else:
                    row_elems = row.find_elements_by_tag_name('td')
                    if len(row_elems) == 2:
                        row_key = row_elems[0]
                        row_value = row_elems[1]
                        if row_key and row_value and section:
                            section[row_key.text] = row_value.text

            if section:
                yield section

    reports = None
    def pre_process_data(self):
        self.reports = []
    def process_data(self, data):
        self.reports.append(data)
