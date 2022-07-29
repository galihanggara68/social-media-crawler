# Social Media Crawler

## Intro

Crawl popular social media data such as Twitter, Facebook, Instagram

## Usage

### Clone or Install from pip

Clone this repo to your current directory

> git clone https://github.com/galihanggara68/social-media-crawler.git

or install using pip

> pip3 install git+https://github.com/galihanggara68/social-media-crawler.git@master

### Import library

First of all import Crawler class and choose your favorite Search Engine

```
from Social_Media_Crawler.search_engines import GoogleSearchEngine
from Social_Media_Crawler.scrapers import TwitterScraper
from Social_Media_Crawler.crawler import Crawler
```

### Using Crawler class

`Crawler` class has 2 parameters `search_engine` the Search Engine class and `social_media` list of social media scraper class

```
# Use TwitterScraper to scrape Twitter Username using limit 5 tweets
t_scraper = TwitterScraper(tweet_limit = 5)

# Instantiate Crawler object with GoogleSearchEngine and TwitterScraper object as social media scraper
crawler = Crawler(GoogleSearchEngine, [t_scraper])

# Search all usernames within "BarisTan" query
data = crawler.crawl("BarisTan")

# Print result
print(data)
```

## Crawler methods

### crawl(name_to_crawl, max_result = 10, delay = 10)

Start executing crawler
