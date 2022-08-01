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
# Use TwitterScraper to scrape Twitter account using limit 5 tweets
t_scraper = TwitterScraper(tweet_limit = 5)

# Use InstagramScraper to scrape Instagram account using limit 3 posts with following username and password for login
i_scraper = InstagramScraper(posts_limit = 3, login_username = "your.instagram.account", login_password = "yourS3cretP4ssw0rd")
scrapers = [t_scraper, i_scraper]

# Create Crawler object with GoogleSearchEngine and preconfigured scrapers
crawler = Crawler(GoogleSearchEngine, scrapers)

# Search all usernames within "BarisTan" query
data = crawler.crawl("BarisTan")

# Print result
print(data)

# Export to JSON file
for i, scraper in enumerate(scrapers):
    data[i].to_json(f'Data_{scraper.get_domain()}.json', orient='records')
```

## Crawler methods

### crawl(name_to_crawl, max_result = 10, delay = 10)

Start executing crawler

## Scrapers Constructor Parameters

### TwitterScraper

```
t_scraper = TwitterScraper(usernames = [], scrape_level = 1, tweet_limit = 1000)
```

### FacebookScraper

```
f_scraper = FacebookScraper(usernames = [], scrape_level = 1, posts_limit = 1000)
```

### InstagramScraper

```
i_scraper = InstagramScraper(usernames = [], login_username = "", login_password = "", scrape_level = 1, posts_limit = 10)
```
