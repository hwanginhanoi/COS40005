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


# domain, created = Domain.objects.get_or_create(name=domain_name)
# if Cache.objects.filter(url=url, visited=True).exists():
#     return
url = "https://mogi.vn/"
driver.get(url)
time.sleep(2)

links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    href = link.get_attribute("href")
    if href and href.startswith(url):
        try:
            print(href)
        except Exception as e:
            continue

