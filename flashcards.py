from logging import error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox import service
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By

from time import sleep

from dotenv import load_dotenv
from os import getenv

load_dotenv()
USERNAME=getenv('UNAME')
PASSWORD=getenv('PWORD')

s = Service('/Users/admin/Documents/git/MEDSAuto/geckodriver')

"""
Steps:
Open Mycourses -> MEDS221 -> content
Manual selection of course (pause until ready)
find element (div id="Slide_Player")
screenshot element
Save to specific folder (as designated at run time)
Probably just manually insert into one note
"""

class doMEDS():
    def __init__(self):

        self.username = USERNAME
        self.password = PASSWORD
        self.count = 0
        self.dName = ""
        self.last_word = ""

        self.browser_options = Options()
        self.browser_options.add_experimental_option("detach", True)  # Make it so the browser doesn't close upon finish
        self._run()

    def _run(self):
        self.driver = webdriver.Firefox(service=s)
        self._login()

    def _login(self):
        self.driver.get("https://mycourses.rit.edu/d2l/home")

        loginbtn = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/table/tbody/tr[1]/td[1]/a')
        loginbtn.click()

        userin = self.driver.find_element(By.XPATH, '//*[@id="username"]')  # Enter username
        userin.send_keys(self.username)
        print("Username Entered:", self.username)

        pwordin = self.driver.find_element(By.XPATH, '//*[@id="password"]')  # Enter pword
        pwordin.send_keys(self.password)
        print('Password Entered', ('*' * len(self.password)))

        submitbtn = self.driver.find_element(By.XPATH, '//*[@id="userInput"]/form/button')  # Submit
        submitbtn.click()
        print("Submitted Login form\n")
        input("Press Enter when you have confirmed 2FA...")
        self._navMeds()

    def _navMeds(self):
        self.driver.get("https://mycourses.rit.edu/d2l/le/content/924392/Home")
        page = input("\nEnter link for current MEDS assignment: ")
        # self.dName = input("Enter folder for assignment: ")
        self.driver.get(page)
        sleep(5)
        self.go_through_flash_cards()

    def go_through_flash_cards(self):
        # while(self.check_next()):
        while True:
            try:
                self.get_text()
                self.next_card()
                sleep(5)
            except Exception as e:
                print(e)
                check = input("Refresh page or new lesson? [r or n] ").lower()
                if check == "r":
                    self.driver.refresh()
                    sleep(5)
                    continue
                elif check == "n":
                    self._restart()
                else:
                    print("Scheiße")
                    break

    def get_text(self):
        titleXPath= "/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div/div[2]/flashcard-question/div/div/div/div[2]/div/div/div[1]/span"
        definitionXPath = "/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div/div[2]/flashcard-question/div/div/div/div[2]/div/div/div[3]/div[1]/span"
        title = self.driver.find_element( By.XPATH, titleXPath).get_attribute('innerHTML')
        definition = self.driver.find_element(By.XPATH, definitionXPath).get_attribute('innerHTML')
        if title != self.last_word:
            with open("flashcards.txt", "a") as f:
                f.write("{} : {}\n".format(title, definition))
        else:
            self._restart()
        
        self.last_word = title

    def next_card(self):
        next_chevronXPath = "/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/button[2]"
        next_chevron = self.driver.find_element(By.XPATH, next_chevronXPath)
        next_chevron.click()

    def _restart(self):
        checkAgain = input("Continuation of lesson or new section? [c or n]]")
        if checkAgain == "n":
            self.count = 0
        self._navMeds()

if __name__ == '__main__':
    mC = doMEDS()
