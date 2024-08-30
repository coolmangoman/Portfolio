import scrapy


class FlixpatrolSpider(scrapy.Spider):
    name = "flixpatrol"
    allowed_domains = ["flixpatrol.com"]
    #start_urls = ["https://flixpatrol.com/most-watched/2023/titles-from-south-korea/"]

    def start_requests(self):
        yield scrapy.Request(url = "https://flixpatrol.com/most-watched/2023/tv-shows-from-south-korea/", callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'})

    def parse(self, response):
        show_container = response.xpath("//tr[@class='table-group']")
        for show in show_container:
            title = show.xpath(".//a[@class='flex gap-2 group items-center']/div[2]/span[1]/text()").get()
            season = show.xpath(".//span[@class='text-sm text-gray-500 whitespace-nowrap']/text()").get()
            hours = show.xpath(".//div[@class='w-36 hidden sm:block text-gray-400 font-semibold']/text()").get()
            runtime = show.xpath(".//td[@class='hidden sm:table-cell table-td w-20 text-sm text-right text-gray-500 table-hover:text-gray-400 tabular-nums']/text()").get()
            views = show.xpath(".//td[@class='table-td text-right text-sm tabular-nums whitespace-nowrap']/div[2]/text()").get()
            show_link = "https://flixpatrol.com" + show.xpath(".//td[@class='table-td w-full']/a/@href").get()
            yield response.follow(
                    url = show_link,
                    callback = self.parse_show,
                    meta = {
                        "title": title,
                        "season": season,
                        "hours": hours,
                        "runtime": runtime,
                        "views": views
                    })
        next_page_url = "https://flixpatrol.com" + response.xpath("//a[@rel='next']/@href").get()
        if next_page_url:
            yield response.follow(url = next_page_url, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'})
            
    def parse_show(self, response):
        title = response.request.meta['title']
        season = response.request.meta['season']
        hours = response.request.meta['hours']
        runtime = response.request.meta['runtime']
        views = response.request.meta['views']
        people_container = response.xpath("//div[@class='card-body space-y-2 text-sm']")
        cast = people_container.xpath("./div/div[2]/a/text()").getall()
        director = people_container.xpath("./div[2]/div[2]/a/text()").get()
        producers = people_container.xpath("./div[3]/div[2]/a/text()").getall()
        creators = people_container.xpath("./div[4]/div[2]/a/text()").getall()
    
        yield {
            "title": title,
            "season": season,
            "hours": hours,
            "runtime": runtime,
            "views": views,
            "cast": cast,
            "director": director,
            "producers": producers,
            "creators": creators
        }
