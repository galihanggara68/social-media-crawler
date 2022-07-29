import time
from googlesearch import search

class GoogleSearchEngine:
    def search(keyword, max_result = 10, delay = 10):
        results = []
        for j in search(keyword, tld="co.id", num=max_result, stop=max_result, pause=delay):
            results.append(j)
        return results

class DuckDuckGoSearchEngine:
    def search(keyword, max_result = 10, delay = 1):
        time.sleep(delay)
        results = ddg(keyword, region='wt-wt', safesearch='Moderate', time='y', max_results=max_result)
        filtered = list(map(lambda obj : obj["href"], results))
        return filtered