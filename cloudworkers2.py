from selenium import webdriver
from time import sleep
import re
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, NoSuchWindowException, WebDriverException, UnexpectedAlertPresentException
# from selenium.webdriver.common.action_chains import ActionChains
import random
import os
import sys
import datetime

class TinderBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())


    def login(self):
        self.driver.get("http://agents.moderationinterface.com/login")

        sleep(2)

        login_button = self.driver.find_element_by_xpath("/html/body/app-root/block-ui/ng-component/div/div/div/div/div/div/div/div/form/div[1]/div/input")
        login_button.click()

        sleep(2)

        email_in = self.driver.find_element_by_xpath("//input[@name='username']")
        email_in.clear()
        email_in.send_keys(self.username)

        pw_in = self.driver.find_element_by_xpath("/html/body/app-root/block-ui/ng-component/div/div/div/div/div/div/div/div/form/div[2]/div/input")
        pw_in.send_keys(self.password)
        pw_in.send_keys(Keys.RETURN)



    def post_comment(self, comment_text,):

        sleep(5)

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath('//*[@id="chat-windows-message-textarea"]')
            comment_box_elem().send_keys("")
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                sleep(random.randint(1, 4) / 90)
        except (NoSuchWindowException, ElementNotInteractableException, UnexpectedAlertPresentException, WebDriverException):
            print('No element of that id present!')
            self.driver.refresh()
            print('Page has been refreshed.')

        try:
            self.driver.find_element_by_xpath("/html/body/app-root/block-ui/ng-component/div/ng-component/div/div/div/div/div[2]/div/form/div[2]/div/div/div/div[2]/div/button").click()
        except (NoSuchElementException, NoSuchWindowException, ElementNotInteractableException, UnexpectedAlertPresentException, WebDriverException):
            print('No element of that id present!')



    """grab comments from a picture page"""

    def get_comments(self):
        # load more comments if button exists
        sleep(5)

        try:
            comments_block = self.driver.find_element_by_class_name('timeline')
            comments_in_block = comments_block.find_elements_by_class_name('timeline-body')
            comments = [x.find_element_by_tag_name('p') for x in comments_in_block]
            user_comment = re.sub(r'#.\w*', '', comments[0].text)
        except (NoSuchElementException, NoSuchWindowException, ElementNotInteractableException, UnexpectedAlertPresentException, WebDriverException):
            return 'nul'
        return user_comment

    """have bot comment on picture"""
    def comment_on_picture(self):
        bot = ChatBot('cloudworkersbot')
        ListTrainer(bot)
        picture_comment = self.get_comments()
        # user's comment and bot's response
        response = bot.get_response(picture_comment).__str__()
        print("User's Comment", picture_comment)
        print("Bot's Response", response)
        dup_items = set()
        uniq_items = []
        for x in response:
            if x not in dup_items:
                uniq_items.append(x)
                dup_items.add(x)
        return self.post_comment(response)

bot = TinderBot(username='EN-1818', password='cRut9yl6afr8cHe')

#while datetime.datetime.now().hour < 9:
if __name__ == '__main__':
    bot.login()
    for i in range(100):
        print(bot.get_comments())
        print("Posted Comment", bot.comment_on_picture())
    os.system("killall -9 'firefox-bin'")
os.execv(sys.executable, ['python'] + sys.argv)

# if __name__ == '__main__':
#    TinderBot()
#    os.execl(sys.executable, sys.executable, *sys.argv)


# Oh darling , actually I just wanted to tell you that you look awesome on your profile pic
