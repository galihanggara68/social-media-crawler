import pandas as pd
import snscrape.modules.twitter as sntwitter
from facebook_scraper import get_posts
import instaloader

class InstagramScraper:
    def __init__(self, usernames = [], login_username = "", login_password = "", scrape_level = 1, posts_limit = 10):
        self.domain = "instagram"
        self.usernames = usernames
        self.scrape_level = scrape_level
        self.posts_limit = posts_limit
        self.instaloader = instaloader.Instaloader()
        self.login_username = login_username
        self.login_password = login_password

    def get_domain(self):
        return self.domain

    def _internal_scrape(self, username, get_linked_users, user_posts, linked_usernames = [], root_username = None):
        profile = instaloader.Profile.from_username(self.instaloader.context, username)
        posts = []
        for i, post in enumerate(profile.get_posts()):
            if i>self.posts_limit: #number of tweets you want to scrape
                break
            if get_linked_users:
                if(len(post.tagged_users) > 0 or len(post.tagged_users) > 0):
                    mentioned_users = post.tagged_users + post.caption_mentions
                    for luname in mentioned_users:
                        if luname not in linked_usernames and luname.strip() != username:
                            print(f"Added {luname}")
                            linked_usernames.append(luname.strip())
            posts.append({"caption": post.caption, "shortcode": post.shortcode, "date": post.date, "url": post.url, "video_url": post.video_url, "caption_hashtags": post.caption_hashtags, "likes": post.likes, "comments": post.comments})
        user_posts.append([profile.username, profile.biography, profile.full_name, profile.followers, profile.followees, posts])

        if get_linked_users:
            for linked in linked_usernames:
                if linked == username:
                    continue
                self._internal_scrape(linked, False, user_posts, linked_usernames, root_username)

    def scrape(self, usernames = []):
        if(len(self.usernames) < 1):
            self.usernames = usernames
        self.instaloader.login(self.login_username, self.login_password)
        arr_usernames = [x["username"] for x in self.usernames]
        user_posts = []
        for username in arr_usernames:
            self._internal_scrape(username, True, user_posts, [], username)
        
        pdf = pd.DataFrame(user_posts, columns=["username", "bio", "full_name", "followers", "followes", "posts"])
        return pdf

class TwitterScraper:
    def __init__(self, usernames = [], scrape_level = 1, tweet_limit = 1000):
        self.domain = "twitter"
        self.usernames = usernames
        self.scrape_level = scrape_level
        self.tweet_limit = tweet_limit
        
    def get_domain(self):
        return self.domain
    
    def _internal_scrape(self, username, get_linked_users = True, tweets = [], linked_usernames = [], root_username = None):
        linked_usernames = []
        print(f"Scraping {username}")
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username}').get_items()): #declare a username 
            if i>self.tweet_limit: #number of tweets you want to scrape
                break
            if get_linked_users:
                if(tweet.mentionedUsers != None):
                    for luname in tweet.mentionedUsers:
                        if luname.username not in linked_usernames and luname.username.strip() != username:
                            print(f"Added {luname.username}")
                            linked_usernames.append(luname.username.strip())
                if tweet.inReplyToUser != None and tweet.inReplyToUser.username.strip() not in linked_usernames and tweet.inReplyToUser.username.strip() != username:
                    print(f"Added {tweet.inReplyToUser}")
                    linked_usernames.append(tweet.inReplyToUser.username.strip())
                if tweet.quotedTweet != None and tweet.quotedTweet.user.username.strip() not in linked_usernames and tweet.quotedTweet.user.username.strip() != username:
                    print(f"Added {tweet.quotedTweet.user.username}")
                    linked_usernames.append(tweet.quotedTweet.user.username.strip())
            tweets.append([tweet.url, tweet.id, tweet.date, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quotedTweet.content if tweet.quotedTweet != None else None, tweet.user, tweet.inReplyToUser.username if tweet.inReplyToUser != None else None, [x.username for x in tweet.mentionedUsers] if tweet.mentionedUsers != None else None, tweet.coordinates, tweet.place, tweet.hashtags, tweet.cashtags])
            
        if get_linked_users:
            for linked in linked_usernames:
                if linked == username:
                    continue
                self._internal_scrape(linked, False, tweets, linked_usernames, root_username)
                
        return tweets
        
    def scrape(self, usernames = [], level = 1):
        if(len(self.usernames) < 1):
            self.usernames = usernames
        tweets_list = []
        arr_usernames = [x["username"] for x in self.usernames]
        for username in arr_usernames:
            self._internal_scrape(username, True, tweets_list, [], username)
        tdf = pd.DataFrame(tweets_list, columns=["url", "id", "date", "content", "replyCount", "retweetCount", "likeCount", "quotedTweet", "user", "inReplyToUser", "mentionedUsers", "coordinates", "place", "hashtags", "cashtags"])
        return tdf


class FacebookScraper:
    def __init__(self, usernames = None, scrape_level = 1, posts_limit = 1000):
        self.domain = "facebook"
        self.usernames = usernames
        self.scrape_level = scrape_level
        self.posts_limit = posts_limit
        
    def get_domain(self):
        return self.domain
        
    def scrape(self, usernames = []):
        fb_posts = []
        if(len(self.usernames) < 1):
            self.usernames = usernames
        for username in self.usernames:
            for i, post in enumerate(get_posts(username["username"], pages=3, extra_info=True, cookies="login.txt")):
                if i>self.posts_limit: #number of tweets you want to scrape
                    break
                fb_posts.append(post)
        fdf = pd.DataFrame(fb_posts, columns = ['post_id', 'text', 'post_text', 'shared_text', 'time', 'image',
       'image_lowquality', 'images', 'images_description', 'images_lowquality',
       'images_lowquality_description', 'video', 'video_duration_seconds',
       'video_height', 'video_id', 'video_quality', 'video_size_MB',
       'video_thumbnail', 'video_watches', 'video_width', 'likes', 'comments',
       'shares', 'post_url', 'link', 'user_id', 'username', 'user_url',
       'is_live', 'factcheck', 'shared_post_id', 'shared_time',
       'shared_user_id', 'shared_username', 'shared_post_url', 'available',
       'comments_full', 'reactors', 'w3_fb_url', 'reactions', 'reaction_count',
       'image_id', 'image_ids', 'fetched_time'])
        return fdf