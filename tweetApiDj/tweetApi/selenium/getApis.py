from typing import Literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

XPATH_OF_RECENT_TWEETS="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div"
XPATH_IMG = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[2]/div/a/div[3]/div/div[2]/div/div"

XPATH_TIME="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a/time"

XPATH_CONTENT='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]'

XPATH_TWEETED_BY = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span"

XPATH_HREF="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div/a"

XPATH_CONTENT2="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[2]/div/span"
class Tweet:
    def __init__(self,imgHtml:str,timeHtml:str,contentHtml:str,tweetedByHtml:str,href:str):
        self.imgHtml = imgHtml
        self.timeHtml = timeHtml
        self.contentHtml = contentHtml
        self.tweetedByHtml = tweetedByHtml
        self.href = href
        
    def to_json(self):
        return {
            "imgHtml":self.imgHtml,
            "timeHtml":self.timeHtml,
            "href":self.href,
            "contentHtml":self.contentHtml,
            "tweetedByHtml":self.tweetedByHtml 
        }



def getRecentTweets(twitterHandle: str):
    browser = webdriver.Chrome()
    browser.get(f'https://twitter.com/{twitterHandle}')
    
    # tweets = browser.find_element_by_xpath(XPATH_OF_RECENT_TWEETS)
    try:
        WebDriverWait(browser, 30).until( EC.element_to_be_clickable((By.XPATH, XPATH_IMG)))
        img = browser.find_element_by_xpath(XPATH_IMG)
        time =browser.find_element_by_xpath(XPATH_TIME).text
        content = browser.find_element_by_xpath(XPATH_CONTENT).get_attribute('outerHTML')
        tweetedBy=browser.find_element_by_xpath(XPATH_TWEETED_BY).text 
        href=browser.find_element_by_xpath(XPATH_HREF).get_attribute('href')
        res = Tweet(
            imgHtml=img.get_attribute('outerHTML'),
            timeHtml=time,
            contentHtml=str(content),
            href=href,
            tweetedByHtml=tweetedBy 
        )
        browser.close()

        return res.to_json()
    except TimeoutException as e:
        print("Wait Timed out")
        print(str(e))
        browser.close()
        return {}
    except Exception as e:
        browser.close()
        print("Something went wrong")
        print(str(e))
        browser.close()
        return {}



if __name__=="__main__":
    s=getRecentTweets("DarrellMello")
    print("/***************************/")
    print(s)
    print("/***************************/")

    s=getRecentTweets("drbeen_medical")
    print("/***************************/")
    print(s)
    print("/***************************/")
