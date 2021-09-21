
# spider = JMASpdier()
# spider = AgoraSpdier()
# spider.execute(name='200301')
from app.spiders.FileExtractionSpider import ScrapySpider

spider = ScrapySpider()
spider.execute(2018, 'YAMAHA','200312')

