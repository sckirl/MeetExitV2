from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from datetime import datetime

# for load time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
        
class MeetExit:
    def __init__(self, driver, url, MINPARTICIPANTS = 20):
        self.driver = driver
        self.url = url
        self.MINPARTICIPANTS = MINPARTICIPANTS
        
    def joinMeet(self):
        self.driver.get(self.url)
        
        try: # try to find the "Join Now" button, if can't find it within 10 seconds then quit
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt"))
            )
            
        except: 
            print("Could not find element")
            self.driver.quit()
            
        finally: 
            sleep(1)
            self.driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL + "d") # close microphone
            sleep(.5)
            self.driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL + "e") # close camera
            
            # enter google meet (click on "Join Now")
            sleep(2)
            self.driver.find_element_by_css_selector(".uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt").click()
            self.checkParticipant()
        
    def checkParticipant(self):
        run = False
        numParticipant = 0
        prevParticipant = 0
        
        # try to find the number of participants in the meeting
        try:
            elem = WebDriverWait(self.driver, float("inf")).until(
                EC.presence_of_element_located((By.CLASS_NAME, "uGOf1d"))
            )
        finally: 
            sleep(2)
            run = True 
            
        # (loop) check the number of participants
        while run:
            # if number of participants <= MINPARTICIPANTS, leave the meeting
            numParticipant = int(self.driver.find_elements_by_class_name("uGOf1d")[0].text)
            
            if numParticipant <= self.MINPARTICIPANTS:
                
                print("-"*50)
                print("Left Meeting at: {}".format(datetime.now()))
                print("-"*50)
                
                run = False
                self.driver.refresh() # refresh the page = leave the meeting
                
            # refresh the printed number only when current number != previous
            if numParticipant != prevParticipant:
                print("Participants: {} | Leave at: {}".format(str(numParticipant), 
                                                                str(self.MINPARTICIPANTS)), 
                                                                end="\r")
                
                prevParticipant = numParticipant

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Users/LENOVO/AppData/Local/Google/Chrome/User Data/Profile 1")
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #ignore warnings

    service = Service("D:\pythonProjects\ClassMate\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    url = input("Enter Meet url: ")
    meetExit = MeetExit(driver, url, 20)

    meetExit.joinMeet() 
    