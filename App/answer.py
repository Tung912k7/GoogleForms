import time
import random

import html
import json
import requests
import time
from time import sleep
import sys
import os
from tqdm import tqdm
from sty import fg, bg, ef
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import welcome
import errors


def getanswer():
    print("freebirdFormviewerComponentsQuestionBaseTitle")

    # Chrome Driver
    data = {}
    checkPath = True
    with open('dependencies.json', 'r') as read_dependencies:
        read_dependencies.seek(0)
        checkPath = read_dependencies.readline(1)
    if not checkPath:
        chromedriver = input(fg(79, 176, 140) + "[~] Please Enter Your Driver Path : ")
        try:
            chromedriverValidated = chromedriver.endswith("chromedriver")
            data['driverPath'] = []
            data['driverPath'].append({
                    'path': chromedriver,
                    'isValidated': True
                })
            with open('dependencies.json', 'w') as write_dependencies:
                    json.dump(data, write_dependencies)
        except:
            if not chromedriverValidated:
                err = errors.geterrors(1)
                exit()
    else:
        with open('dependencies.json', 'r') as read_dependencies_path:
            mainData = json.load(read_dependencies_path)
            pathData = mainData['driverPath'][0]['path']
            chromedriver =  pathData

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    # Target Form
    userlink = input(fg(79, 176, 140) + "[~] Enter Your Google Form Url: ")
    verifiedlink = userlink.startswith("https://docs.google.com/forms/") or userlink.startswith("https://forms.gle")

    
    # Get Link
    if driver.get(userlink):
        for i in tqdm(range(5)):
            sleep(0.2)
    
    # Link Verification
    if not verifiedlink:
        err = errors.geterrors(2)
        exit()
    
    

    # Target Options
    req = requests.get(userlink)
    soup = BeautifulSoup(req.content, "html.parser")

    print(fg(0, 255, 145) + "\n[!] Looking For Questions ... \n")

    questioncount = 0
    answercount = 0
    allquestions = ["sample"]
    allanswers = ["sample"]

    for questions in soup.find_all("div", class_="freebirdFormviewerComponentsQuestionBaseTitle"):
        questioncount = questioncount + 1
        convertquestioncount = str(questioncount)
        allquestions.append(questions.text)

    for answers in soup.find_all("span", class_="freebirdFormviewerComponentsQuestionRadioLabel") or soup.find_all("span", class_="freebirdFormviewerComponentsQuestionCheckboxLabel"):
        answercount = answercount + 1
        convertanswercount = str(answercount)
        allanswers.append(answers.text)
    
    print("Found {0} Questions !".format(convertquestioncount))
    print("Found {0} Answers !".format(convertanswercount))


    # Search Answers

    if questioncount or answercount > 0 :
        print("Looking For Answers ...")

        checkboxpath = None
        answernum = len(allanswers)
        if soup.find_all("span", class_="freebirdFormviewerComponentsQuestionCheckboxLabel"):
            choices = driver.find_elements_by_class_name("freebirdFormviewerComponentsQuestionCheckboxLabel")
            for i in range(0, len(choices)):
                if choices[i].is_displayed():
                    choices[i].click()


        radiolabelspath = None
        if soup.find_all("span", class_="freebirdFormviewerComponentsQuestionRadioLabel"):
            choices = driver.find_elements_by_class_name("freebirdFormviewerComponentsQuestionRadioLabel")
            for i in range(0, len(choices)):
                if choices[i].is_displayed():
                    choices[i].click()

        # Submit Automation
        submitpath = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div/div/span'
        submit = driver.find_element_by_xpath(submitpath)
        webdriver.ActionChains(driver).move_to_element(submit).click(submit).perform()
        print("Submited Form !!!")

        # Click ViewScore
        sleep(3.5)
        viewscorepath = "/html/body/div[1]/div[2]/div[1]/div/div[4]/div/a/span/span"
        viewscore = driver.find_element_by_xpath(viewscorepath)
        webdriver.ActionChains(driver).move_to_element(viewscore).click(viewscore).perform()
        print("Clicked ViewScore !!!")

        # Find Answers
        sleep(1)
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdiwAWqBjTPQfAYiiK98Ttex6QRjJ7lAhA7CGU4wTlItmBShw/viewscore?viewscore=AE0zAgAtBzriNp-WZEzlULNAhMQnSOioffHO0OfkO7r3Yt10T4jFK6-rTXJ4rpgXebUKplQ")
        sleep(3)


        finddivs = driver.find_elements_by_class_name("freebirdFormviewerViewItemsCheckboxLabel")
        findanswers = driver.find_elements_by_class_name("freebirdFormviewerViewItemsCheckboxLabel")

        foundanswer = None
        if findanswers:
            for i in range(1, len(finddivs)):
                foundanswer = '/html/body/div/div[2]/div[1]/div/div[2]/div[{0}]/div/div[4]/div[2]/div/label/div/div[2]/div/span'.format(str(i))
                target = driver.find_element_by_xpath(foundanswer)
                if target.is_displayed():
                    print(target.text)
                else:
                    print("Already Correct !")

    else:
        print(fg(255, 76, 36) + "No Questions or Answers Found !")

