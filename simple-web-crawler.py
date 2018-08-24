import argparse
import re

from graphviz import Digraph
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
graph = Digraph()


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


def make_node_name(url):
    # problems with Graphviz node names
    name = "\"" + url + "\""
    name = name.replace("://", ".")
    return name

class SimpleSpider(CrawlSpider):
    name = 'simplespider'

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True,),
    )

    def parse_start_url(self, response):
        graph.node(make_node_name(response.request.url), label=make_node_label(response))
        request = super(SimpleSpider, self).parse_start_url(response)
        return request

    def _requests_to_follow(self, response):
        for r in super(SimpleSpider, self)._requests_to_follow(response):
            r.meta["parent_url"] = response.request.url
            yield r


    def parse_item(self, response):
        current_url = make_node_name(response.request.url)
        parent_url = make_node_name(response.meta["parent_url"])
        # print "Parsed page: %s" % current_url, "Parent page: %s" % parent_url
        graph.node(current_url, label=make_node_label(response))
        graph.edge(parent_url, current_url)


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
    graph.format = "svg"
    graph.render(arguments.output_filename)



if __name__ == '__main__':
    main()
