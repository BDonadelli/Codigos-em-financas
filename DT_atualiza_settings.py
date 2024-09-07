'''
  biblioteca e configuração para pegar dados
  - iteragir com google sheets
  - web scraping com selenium
'''
import pandas as pd
import os
data_path = str(os.getcwd()) + r"/data/"

from time import sleep
from datetime import date
today = date.today().strftime('%d/%m/%Y')

## - google sheets -----------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

## - selenium -----------------

from selenium import webdriver
from selenium.webdriver.common.by import By

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
opts.add_experimental_option("prefs", {
  "download.default_directory": data_path,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

# driver=webdriver.Chrome(options=opts)
