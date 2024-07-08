import time
from sys import stdout
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from .models import Property, Domain, Cache


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)



