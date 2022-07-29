import re

class Crawler:
    def __init__(self, search_engine, social_media = []):
        self.search_engine = search_engine
        self.social_media = social_media
        self.results = []
        
    def crawl(self, name_to_crawl, max_result = 10, delay = 10):
        self.urls = self.search_engine.search(name_to_crawl, max_result, delay)
        self.usernames = self.extract_username_from_urls(urls = self.urls, urls_pattern = ['https://.*(instagram|facebook|twitter)\.com\/([A-Za-z0-9-.\_]+)', 'https://.*(linkedin)\.com\/in/([A-Za-z0-9-.\_]+)'])
        print(self.usernames)
        self.exec_scrape()
        return self.results
        
    def extract_username_from_urls(self, urls, urls_pattern):
        results = []
        for url in urls:
            for pattern in urls_pattern:
                result = re.search(pattern, url)
                if result:
                    results.append({"domain": result.group(1), "username": result.group(2)})
                    break
        return results
    
    def filter_username_by_domain(self, usernames, domain):
        return list(filter(lambda id: id["domain"] == domain, usernames))
    
    def exec_scrape(self):
        for social in self.social_media:
            usernames = self.filter_username_by_domain(self.usernames, social.get_domain())
            self.results.append(social.scrape(usernames))