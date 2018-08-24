# Simple Web Crawler

![](https://img.shields.io/badge/python-2.7-blue.svg) ![](https://img.shields.io/badge/dep-scrapy-yellowgreen.svg) ![](https://img.shields.io/badge/dep-graphviz-lightgrey.svg)

A very very simple web crawler. Take in input an URL and outputs the site map. It uses Scrapy and PyGraphviz.

It ignores URLs of a different domain from the starting url.

## Installation
Please follow the installation guide of 
[Scrapy](https://docs.scrapy.org/en/latest/intro/install.html#platform-specific-installation-notes)
 and [Graphviz](https://www.graphviz.org/download/).

Then, run the following:

    pip install -r requirements.txt

## Usage

    $python2 simple-web-crawler.py -h
    usage: simple-web-crawler.py [-h] [-o output_filename] url

E.g.:

    python2 simple-web-crawler.py https://www.lipsum.com/


You can find the map in `output.svg` and in DOT format in `output`.