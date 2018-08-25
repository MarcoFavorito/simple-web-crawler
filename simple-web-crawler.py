import argparse
import re

from pygraphviz import *
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

parser = argparse.ArgumentParser(description='A very simple web crawler')
parser.add_argument('url', metavar='url', type=str,
                    help='The url of the page where to start.')
parser.add_argument('-o', metavar='output_filename', dest="output_filename", type=str, default="output",
                    help='The output filename.')

arguments = parser.parse_args()
graph = AGraph(directed=True, rankdir="LR")


def extract_domain(url):
    try:
        domain = next(re.finditer(":\/\/[^/]+", url)).group()[3:]
        return domain
    except Exception as e:
        return None


def extract_title(response):
    try:
        title = Selector(text=response.body).xpath('//title/text()').extract()[0]
        title = title.strip()
        return title
    except Exception as e:
        return ""


def make_node_label(response):
    return (extract_title(response) + "\n" + response.request.url).strip()


class SimpleSpider(CrawlSpider):
    name = 'simplespider'

    rules = [Rule(LinkExtractor(), callback='parse_item', follow=True,)]
    # custom_settings = {'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}

    def parse_start_url(self, response):
        graph.add_node(response.request.url, label=make_node_label(response))
        request = super(SimpleSpider, self).parse_start_url(response)
        return request

    def _requests_to_follow(self, response):
        for r in super(SimpleSpider, self)._requests_to_follow(response):
            r.meta["parent_url"] = response.request.url
            yield r

    def parse_item(self, response):
        current_url = response.request.url

        # https://github.com/scrapy/scrapy/issues/15: Scrapy does not filter redirections
        if extract_domain(current_url) != self.allowed_domains[0]:
            return
        graph.add_node(current_url, label=make_node_label(response))

        parent_url = response.meta["parent_url"]
        graph.add_edge(parent_url, current_url)


def main():

    start_url = arguments.url
    domain = extract_domain(start_url)
    if domain is None:
        print "Error: Cannot find domain name in the url."
        exit(1)

    print "Starting url: %s" % start_url
    print "Domain: %s" % domain

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(SimpleSpider, start_urls=[start_url], allowed_domains=[domain])
    process.start()  # the script will block here until the crawling is finished

    graph.graph_attr["rankdir"] = "LR"
    graph.layout("dot")
    graph.draw(arguments.output_filename, format="svg")



if __name__ == '__main__':
    main()
