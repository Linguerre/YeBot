from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.webdriver.common.by import By
import time

class YeBot:

    def __init__(self, youtube_email, youtube_password, twitter_handle, tweet_limit):
        self.bot = webdriver.Firefox()
        self.login_details = {
            "youtube_email" : youtube_email,
            "youtube_password" : youtube_password}
        self.twitter_handle = twitter_handle
        self.tweet_limit = self.limit_check(tweet_limit)
        self.tweets = []
        self.trending_videos = []

    def get_tweets(self):
        bot = self.bot
        bot.get(f"https://twitter.com/{self.twitter_handle}")
        tweets = []     
        try:

            WebDriverWait(bot, 20).until(exp_cond.presence_of_element_located((By.XPATH, '//div[@data-testid="tweet"]')))

            while len(self.tweets) < self.tweet_limit:                
                WebDriverWait(bot, 100).until(exp_cond.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweet"]')))
                time.sleep(10)
                
                # Collect the tweets
                tweets = bot.find_elements_by_xpath('//div[@data-testid="tweet"]/child::div[2]/child::div[2]/div[1]/div[1]')
                self.tweets.extend([tweet.text for tweet in tweets if len(tweet.text) > 1])

                print(f"Size of tweets: {len(tweets)} Size of ye_tweets: {len(self.tweets)}")
                bot.execute_script("window.scrollBy(0, document.body.scrollHeight)")

            self.tweets = [i for n, i in enumerate(self.tweets) if i not in self.tweets[:n]] 
               
        except Exception as ex:
            print(ex)
            bot.quit()

    def post_tweets_to_trending_videos(self):

        if len(self.tweets):
            try:
                bot = self.bot
                bot.get("https://www.youtube.com/")

                #Sign in
                WebDriverWait(bot, 30).until(exp_cond.element_to_be_clickable((By.XPATH, '//paper-button[@aria-label="Sign in"]'))).click()

                WebDriverWait(bot, 30).until(exp_cond.presence_of_all_elements_located((By.XPATH, '//input[@type="email" or @id="identifierId"]')))
                email = bot.find_element_by_xpath('//input[@type="email" or @id="identifierId"]')
                email.clear()
                email.send_keys(self.login_details["youtube_email"])
                email.send_keys(Keys.RETURN)

                WebDriverWait(bot, 100).until(exp_cond.element_to_be_clickable((By.XPATH, '//form[@method="post" or @method="POST"]//input[@type="password"]'))).click()
                password = bot.find_element_by_xpath('//form[@method="post" or @method="POST"]//input[@type="password"]')
                password.clear()
                password.send_keys(self.login_details["youtube_password"])
                password.send_keys(Keys.RETURN)

                # Go to trending
                WebDriverWait(bot, 30).until(exp_cond.element_to_be_clickable((By.XPATH, '//a[@title="Trending"]'))).click()
                WebDriverWait(bot, 100).until(exp_cond.presence_of_all_elements_located((By.XPATH, '//a[@id="video-title"]')))
                time.sleep(10)
                trending_videos = bot.find_elements_by_xpath('//a[@id="video-title"]')        
                self.trending_videos.extend([vids.get_attribute("href") for vids in trending_videos])   

                counter = 0

                while counter < self.tweet_limit:
                    try:               
                        bot.get(self.trending_videos[counter])

                        WebDriverWait(bot, 500).until(exp_cond.presence_of_all_elements_located((By.ID, "placeholder-area")))
                        bot.find_element_by_id("placeholder-area").click()
                        comment_field = bot.find_element_by_xpath('//yt-formatted-string[@id="contenteditable-textarea"]/div[@id="contenteditable-root"]')
                        comment = self.tweets[counter]
                        comment_field.send_keys(comment)
                        bot.find_element_by_xpath('//ytd-button-renderer[@id="submit-button"]').click()
                        time.sleep(5)
                        

                    except Exception as ex:
                        print(ex)   

                    finally:
                        counter += 1      
                        print(counter)
                        time.sleep(10)

            
            except Exception as ex:
                print(ex)

    def limit_check(self, tweet_limit):
        if tweet_limit >= 1 and tweet_limit <= 50:
            return tweet_limit
        
        elif tweet_limit > 50:
            return 50
        
        else:
            return 1 


yebot = YeBot("yourbotaccount@gmail.com", "yourbotPASSWORD", "kanyewest", 20)
yebot.get_tweets()
yebot.post_tweets_to_trending_videos()