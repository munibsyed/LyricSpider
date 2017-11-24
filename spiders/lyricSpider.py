import scrapy
from languageFilter import LanguageFilter
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

'''
Munib Syed, 25/11/2017
Currently, the spider can take in a link to an album on genius.com, iterate through all the songs in the tracklist and extract all relevant lyric text.
It can then perform some language filtering / categorization on this text. The language filtering is in a fairly untested state at the moment.
Currently, I have only tested a handful of albums, but results seem consistent across different inputs.
'''
#global language filter instance
languageFilter = LanguageFilter()

class LyricSpider(scrapy.Spider):

    name = "LyricSpider"
    start_urls = ["https://genius.com/Kendrick-lamar-damn-tracklist-album-art-lyrics"]
    def parse(self, response):
        #this only works for the tracklist page.
        #should be re-written for the main album page
        for div in response.css("div.track_listing-track"):
            #get href (<a href=...>)
            href = div.css("a::attr(href)")
            yield scrapy.Request(href.extract_first(),
                                 callback=self.parse_song_page,
                                 errback=self.errback_httpbin)

    def parse_song_page(self, response):

        title = response.css("title::text").extract_first()
        lyricsDiv = response.css("div.lyrics")
        #the period is necessary so it only finds paragraphs that are children of lyricsDiv
        lyrics = lyricsDiv.select('.//p//text()')
        lyricsJoined = ""
        for l in lyrics:
            lyricsJoined += l.extract()
        
        yield { "Title" : title, "Is Clean: " : languageFilter.is_dirty(lyricsJoined) }
   
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
