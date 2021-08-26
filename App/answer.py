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
    print("Started Secret Finder !!!")
    