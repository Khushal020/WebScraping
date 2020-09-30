import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class FakingNewsExtract():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://www.fakingnews.com/')
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()
        
    
    def extractPolitics(self): #this function extracts links of articles related to politics
        self.driver.find_element_by_xpath("//a[@href='http://www.fakingnews.com/category/politics']").click()

        while(True):
            try:
                self.driver.find_element_by_xpath("//*[@id='ldm_cat']/a").click()
            except NoSuchElementException:
                break
            except ElementNotInteractableException:
                break
        
        politics_articles = self.driver.find_elements_by_xpath("//*[@class='story-box']/div/h2/a")
        
        
    def extractSub(self, sub): #Thid is general function for all subjects
        #this line is for clicking on link for that perticular subjects
        self.driver.find_element_by_xpath("//a[@href='http://www.fakingnews.com/category/{0}']".format(sub)).click()
        
        #this loop is for clicking on that 'MORE' button until it does not show up
        while(True):
            try:
                self.driver.find_element_by_xpath("//*[@id='ldm_cat']/a").click()
            except NoSuchElementException:
                break
            except ElementNotInteractableException:
                break
        #this line will get list of link of that all articles
        articles = self.driver.find_elements_by_xpath("//*[@class='story-box']/div/h2/a")
        articles = [i.get_attribute('href') for i in articles]
        return articles
        
    #this funtion extracts link for all subjects in variable subs
    def extractSubs(self, subs):
        artilce_list = []
        for i in subs:
            articles = self.extractSub(i)
            artilce_list += articles
            print('{0} shape {1}'.format(i, len(articles)))
            
        return artilce_list
            
    #this function is to create csv file of list of link
    def createCSV(self, articles, name):
        with open('{0}_list.csv'.format(name), 'w', newline='') as myfile:
            art_list_csv = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i in articles:
                art_list_csv.writerow([i,])
        
bot = FakingNewsExtract()
subs = ['politics']
        #, 'society', 'media', 'social-media', 'entertainment', 'sports', 'technology', 'business', 'world', 'snippets', 'features']

articles = bot.extractSubs(subs)
bot.createCSV(articles, 'articles')