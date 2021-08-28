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
    allquestions = ["Please Select From Available Answers"]
    allanswers = ["Please Select From Available Answers"]

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
    