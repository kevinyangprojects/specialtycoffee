import scrapy
import re
URL = 'https://www.fourkilofish.com.au'

"""
    Notes: Hard code fix for Geisha beans because of inconsistent formatting
    Can be improved to parse the actual text and not the HTML structure
"""

class FourKiloSpider(scrapy.Spider):
    name = "four_kilo"

    def start_requests(self):
        urls = [
            'https://www.fourkilofish.com.au/collections/exclusive-single-origin-yunnan'
        ]
        # For each of the URLs, the HTML page is scraped
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    ## This section extracts all of the links for each of the coffees available
    def parse(self, response):

        ## Extracts all of the coffee item links from the main page
        for link in response.css('div.grid__item.large--one-half div div a::attr(href)').getall():
            ## Uses different call back to parse individual items
            yield scrapy.Request(URL+link, self.parse_news)


    def strip_elements(self, text):
        """
            Returns the text in the element.
        """
        return re.sub("<[^>]+>", "", text).strip()

    def parse_news(self, response):
        ## Gets all of the information in the piped format
        textInfo = response.css('h1.product-details-product-title').getall()[0]
        textInfo = self.strip_elements(textInfo).split(" | ")

        ## Gets each individual piece of text information, only 4 key pieces of info.
        if len(textInfo) == 4:
            name, process, origin, weight = textInfo
        else:
            ## Hard code fix for Geisha beans
            name, origin, process, weight = textInfo[-4:]

        itemPrice = response.css('span#ProductPrice').getall()[0]
        itemPrice = self.strip_elements(itemPrice)

        ## Return JSON information of coffee item
        yield{
            'name' : name,
            'process' : process,
            'origin' : origin,
            'weight' : weight,
            'price' : itemPrice
        }


