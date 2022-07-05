import os
from typing import Literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


XPATH_OF_RECENT_TWEETS="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div"
XPATH_IMG = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[2]/div/a/div[3]/div/div[2]/div/div"

XPATH_TIME="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a/time"

XPATH_CONTENT='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]'

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


def  load_driver():
	options = webdriver.FirefoxOptions()
	
	# enable trace level for debugging 
	options.log.level = "trace"

	options.add_argument("-remote-debugging-port=9224")
	options.add_argument("-headless")
	options.add_argument("-disable-gpu")
	options.add_argument("-no-sandbox")

	binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

	firefox_driver = webdriver.Firefox(
		firefox_binary=binary,
		executable_path=os.environ.get('GECKODRIVER_PATH'),
		options=options)

	return firefox_driver

def getRecentTweets(twitterHandle: str):

    # options = Options()
    # options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # # =str(os.environ.get('CHROMEDRIVER_PATH'))
    # # s=Service(ChromeDriverManager().install())
    # browser = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)
    browser= load_driver()
    # browser = webdriver.Chrome(service=s, options=options)

    browser.get(f'https://twitter.com/{twitterHandle}/')
    
    # tweets = browser.find_element_by_xpath(XPATH_OF_RECENT_TWEETS)
    try:
        WebDriverWait(browser, 10).until( EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
        img = browser.find_element_by_xpath(XPATH_IMG)
        time =browser.find_element_by_xpath(XPATH_TIME).text
        content = browser.find_element_by_xpath(XPATH_CONTENT).text
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
    except:
        browser.close()
        print("Something went wrong")
        browser.close()
        return {}



if __name__=="__main__":
    s=getRecentTweets("DarrellMello")
    print("/**************************/")
    print(s)
    print("/***************************/")

    s=getRecentTweets("GVDBossche")
    print("/***************************/")
    print(s)
    print("/***************************/")
