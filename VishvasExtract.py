from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class VishvasExtract():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.vishvasnews.com/')
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Accept')]")))
        self.driver.find_element_by_xpath("//button[contains(text(),'Accept')]").click()
        self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/ul/li[2]/a').click()
        
        #self.news_type = ['politics','Society','World','Viral','Health']
    
    def ExtractPolitics(self):
        self.driver.find_element_by_xpath("//a[@href='https://www.vishvasnews.com/english/politics/']").click()

        while(True):
            try:
                self.driver.find_element_by_xpath("//a[contains(text(),'Load More')]").click()
            except NoSuchElementException:
                break
        
        politics_articles = self.driver.find_elements_by_xpath("//*[@class='imagecontent']/h3/a")
        
        
bot = VishvasExtract()