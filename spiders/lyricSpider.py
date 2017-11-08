import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class LyricSpider(scrapy.Spider):

    name = "LyricSpider"
    start_urls = ["https://genius.com/Lupe-fiasco-lupe-fiascos-food-and-liquor-tracklist-album-art-lyrics"]

    def parse(self, response):

        for div in response.css("div.track_listing-track"):
            #get href (<a href=...>)
            href = div.css("a::attr(href)")
            yield scrapy.Request(href.extract_first(),
                                 callback=self.parse_song_page,
                                 errback=self.errback_httpbin)

    def parse_song_page(self, response):
        
        lyricsDiv = response.css("div.lyrics")
        #the period is necessary so it only finds paragraphs that are children of lyricsDiv
        lyrics = lyricsDiv.select('.//p//text()')
        lyricsJoined = ""
        for l in lyrics:
            lyricsJoined += l.extract()
            
        yield { "Lyrics" : lyricsJoined }
        


    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
