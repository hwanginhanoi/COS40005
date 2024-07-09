# import time
# from sys import stdout
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

from cos40005.models import Domain
from tasks import crawl_content
# from .models import Property, Domain, Cache


# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)


# domain, created = Domain.objects.get_or_create(name=domain_name)
# if Cache.objects.filter(url=url, visited=True).exists():
#     return
# url = "https://mogi.vn/"
# driver.get(url)
# time.sleep(2)
#
# links = driver.find_elements(By.TAG_NAME, "a")
# for link in links:
#     href = link.get_attribute("href")
#     if href and href.startswith(url):
#         try:
#             print(href)
#         except Exception as e:
#             continue
#


domains = Domain.objects.all()
if len(domains) > 0:
    domain = domains[0]

crawl_content(domain, 'https://mogi.vn/quan-7/thue-can-ho-chung-cu/tong-hop-nhieu-can-ho-sky-garden-cho-thue-thang-07-2024-id22596688')



