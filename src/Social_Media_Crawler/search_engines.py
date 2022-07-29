import time
from googlesearch import search

class ISearchEngine(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'search') and 
                callable(subclass.load_data_source))

class GoogleSearchEngine(ISearchEngine):
    def search(keyword, max_result = 10, delay = 10):
        results = []
        for j in search(keyword, tld="co.id", num=max_result, stop=max_result, pause=delay):
            results.append(j)
        return results

class DuckDuckGoSearchEngine(ISearchEngine):
    def search(keyword, max_result = 10, delay = 1):
        time.sleep(delay)
        results = ddg(keyword, region='wt-wt', safesearch='Moderate', time='y', max_results=max_result)
        filtered = list(map(lambda obj : obj["href"], results))
        return filtered