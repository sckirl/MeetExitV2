from selenium import webdriver
import time
from MeetExit import *
from datetime import datetime

# for load time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClassMate:
    def __init__(self, start: datetime.time, end: datetime.time):
        # Constants
        self.PRESENCEURL    = "YOUR PRESENCE URL"
        self.CLASSROOMURL   = "YOUR CLASSROOM URL"
        self.DRIVERPATH     = "CHROME DRIVER DIRECTORY"
        self.USERDATADIR    = "user-data-dir=C:/Users/ YOUR_USERNAME /AppData/Local/Google/Chrome/User Data/ CHROME PROFILE"
        
        self.start = start # start of the session/school
        self.end = end     # end of session/school
        
        # Credit: https://stackoverflow.com/a/43714191
        options = webdriver.ChromeOptions()
        options.add_argument(self.USERDATADIR)
        options.add_experimental_option('excludeSwitches', ['enable-logging']) #ignore warnings

        self.driver = webdriver.Chrome(executable_path=self.DRIVERPATH, options=options)
        
    def update(self):
        # (now - start) time, in minutes
        mins = (datetime.now() - self.start).total_seconds()//60
        
        # refresh the page every (now - start) == 20 minutes
        if mins % 20 == 0 and \
           (self.start <= datetime.now() and datetime.now() <= self.end):
               self.presence()
               time.sleep(2)
               self.classLatest()
            
        time.sleep(60)
              
    def presence(self): 
        # get new tab
        self.driver.execute_script("window.open()")
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])
        
        # go to the PRESENCEURL url
        self.driver.get(self.PRESENCEURL)
        
        # click on a button from that url
        BUTTON = ".appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel"
        try:
            WebDriverWait(self.driver, float("inf")).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON)))
        finally:
            self.driver.find_element_by_css_selector(BUTTON).click()
        
        time.sleep(1)
        self.driver.execute_script("window.close()") # close the tab
        self.driver.switch_to.window(tabs[0])
    
    def classLatest(self):
        # get the latest update from google classroom
        self.driver.get(self.CLASSROOMURL)
        try:
            WebDriverWait(self.driver, float("inf")).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".n4xnA")))
        finally:
            self.driver.find_element_by_css_selector(".n4xnA").click()
        
        # check for google meet url
        try:
            WebDriverWait(self.driver, float("inf")).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "t2wIBc")))
            
        finally:
            blocks = self.driver.find_elements_by_class_name("t2wIBc")
            for block in blocks:
                # check for google meet link in classroom
                url = block.text.split()[-1]
                print(url, url[:24])
                if url[:24] == "https://meet.google.com/":
                    print("what teh asidjfilawdjilf")
                    # join the google meet and check for number of participants inside
                    meetExit = MeetExit(self.driver, url, 20)
                    meetExit.joinMeet()
    
if __name__ == "__main__":
    now = datetime.now()
    DATE = now.strftime(" %Y/%m/%d")
    
    # should be in the same month, year, and day
    START = datetime.strptime('07:30' + DATE, '%H:%M  %Y/%m/%d')
    END = datetime.strptime('15:20' + DATE, '%H:%M  %Y/%m/%d')

    classMate = ClassMate(START, END)
    while True:
        classMate.update()